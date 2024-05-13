
from contextlib import contextmanager
from pathlib import Path
import re
import subprocess
import sys
from tempfile import NamedTemporaryFile

from babel.support import Format, Translations
import jinja2
from packaging.version import Version

from .templating import templated_text


__all__ = ['generate_pdf', 'is_weasyprint_available']

_weasyprint_version = None

def is_weasyprint_available():
    try:
        process = subprocess.run(['weasyprint', '--version'], capture_output=True, shell=False)
    except FileNotFoundError:
        return False
    global _weasyprint_version
    _weasyprint_version = _extract_weasyprint_version(process.stdout)
    return True


def _extract_weasyprint_version(weasyprint_stdout):
    version_pattern = br'WeasyPrint version (\d+\.\d+)$'
    match = re.search(version_pattern, weasyprint_stdout.strip())
    if not match:
        sys.stderr.write('Could not determine WeasyPrint version\n')
        sys.stderr.write('Output of "weasyprint --version": %r\n' % weasyprint_stdout)
        sys.exit(10)
    version_str = match.group(1).decode('ascii')
    # LATER: check for minimum version (pdf-identifier)
    return Version(version_str)


def build_formatter(locale, currency):
    _format = Format(locale=locale)
    _format.amount = lambda v: _format.currency(v, currency=currency)
    return _format

def generate_pdf(invoice, invoice_cfg, target_path, *, with_logo=False):
    template_path = Path(invoice_cfg['template'])
    template_dir = template_path.parent
    template = load_invoice_template(template_path, locale=invoice.language)
    _format = build_formatter(invoice.language, currency=invoice.currency)
    template_params = {
        'tt': lambda text, dbobj: templated_text(text, dbobj, _format),
        'f': _format,
        **invoice_cfg,
        'with_logo': with_logo,
    }

    html_str = template.render(invoice=invoice, **template_params)
    with store_generated_html(template_dir, html_str) as path_html:
        cmd = ['weasyprint', str(path_html.absolute()), str(target_path.absolute())]
        subprocess.run(cmd, shell=False, cwd=template_dir)

def load_invoice_template(template_path, locale=None):
    tmpl_loader = jinja2.FileSystemLoader(searchpath=template_path.parent)
    tmpl_env = jinja2.Environment(
        loader=tmpl_loader,
        extensions=['jinja2.ext.i18n'],
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=True,
        undefined=jinja2.StrictUndefined,
    )
    if locale:
        locale_dir = (template_path.parent / 'i18n')
        translations = Translations.load(dirname=locale_dir, locales=[locale], domain='pyinvoice')
        tmpl_env.install_gettext_translations(translations)
    return tmpl_env.get_template(template_path.name)

@contextmanager
def store_generated_html(template_path, html_str) -> Path:
    with NamedTemporaryFile(dir=template_path, mode='w', suffix='.html') as temp_fp:
        temp_fp.write(html_str)
        temp_fp.seek(0)
        yield Path(temp_fp.name)

