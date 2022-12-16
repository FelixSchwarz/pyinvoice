'''Generate PDF invoices from XML files.

Usage:
    pyinvoice [options] [--ignore=<KEY>]... <INVOICE> [<PDF>]
    pyinvoice --version

Arguments:
    --config=<CFG>    Path to configuration file (default: ./invoicing.ini)
    --with-logo       Include logo in PDF invoice
'''

from importlib.metadata import version
from pathlib import Path
import sys

from docopt import docopt

from .check import check_invoice, MetaInfo
from .config import parse_config
from .parser import InvoiceParser
from .pdf_generator import generate_pdf, is_weasyprint_available


__all__ = ['cli_main']

def cli_main():
    args = docopt(__doc__)
    show_version = args['--version']
    if show_version:
        version_str = version('pyinvoice')
        print(version_str)
        return

    path_invoice_xml = args['<INVOICE>']

    if not Path(path_invoice_xml).exists():
        sys.stderr.write('Invoice file "%s" does not exist.\n' % path_invoice_xml)
        sys.exit(1)
    path_cfg = args['--config']
    if path_cfg:
        if not Path(path_cfg).exists():
            sys.stderr.write('Configuration file "%s" does not exist.\n' % path_cfg)
            sys.exit(1)
    else:
        default_cfg = Path('./invoicing.ini')
        if not default_cfg.exists():
            sys.stderr.write('No configuration file found: Please use "--config=...".')
            sys.exit(2)
        path_cfg = str(default_cfg)

    ignored_errors = args['--ignore']
    with_logo = args['--with-logo']
    # == 'None' because argopt 0.7.1 uses that in case the user did not specify
    # the value explicitely
    pdf_path = args['<PDF>']
    if (not pdf_path) or (pdf_path == 'None'):
        suffix = ('.logo' if with_logo else '') + '.pdf'
        pdf_path = Path(path_invoice_xml).with_suffix(suffix)
    else:
        pdf_path = Path(pdf_path)

    invoice = InvoiceParser.parse(filename=path_invoice_xml)
    invoice_cfg = parse_config(path_cfg)

    config_dir = Path(path_cfg).parent
    meta = MetaInfo(config=invoice_cfg, config_dir=config_dir, invoice_filename=path_invoice_xml)
    errors = check_invoice(invoice, meta)
    if errors:
        found_error = False
        for error in errors:
            if error.key not in ignored_errors:
                print(error.message)
                found_error = True
        if found_error:
            return

    if not is_weasyprint_available():
        print('"weasyprint" not found, please install the weasyprint package.')
        return

    generate_pdf(invoice, invoice_cfg, target_path=pdf_path, with_logo=with_logo)

