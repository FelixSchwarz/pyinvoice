
from contextlib import contextmanager
from pathlib import Path
import subprocess
from tempfile import NamedTemporaryFile

from babel.support import Format
import jinja2


__all__ = ['generate_pdf']

def generate_pdf(invoice, invoice_cfg, target_path, *, with_logo=False):
    template_path = Path(invoice_cfg['template'])
    template_dir = template_path.parent
    template = load_invoice_template(template_path)
    _format = Format(locale=invoice.language)
    _format.amount = lambda v: _format.currency(v, currency=invoice.currency)
    template_params = {'f': _format, **invoice_cfg, 'with_logo': with_logo}

    html_str = template.render(invoice=invoice, **template_params)
    with store_generated_html(template_dir, html_str) as path_html:
        cmd = ['weasyprint', str(path_html.absolute()), str(target_path.absolute())]
        subprocess.run(cmd, shell=False, cwd=template_dir)

def load_invoice_template(template_path):
    tmpl_loader = jinja2.FileSystemLoader(searchpath=template_path.parent)
    tmpl_env = jinja2.Environment(
        loader=tmpl_loader,
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=True,
        undefined=jinja2.StrictUndefined,
    )
    return tmpl_env.get_template(template_path.name)

@contextmanager
def store_generated_html(template_path, html_str) -> Path:
    with NamedTemporaryFile(dir=template_path, mode='w', suffix='.html') as temp_fp:
        temp_fp.write(html_str)
        temp_fp.seek(0)
        yield Path(temp_fp.name)
