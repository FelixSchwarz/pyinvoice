'''Generate PDF invoices from XML files.

Usage:
    pyinvoice [options] [--ignore=<KEY>]... <INVOICE> [<PDF>]
    pyinvoice --version

Arguments:
    --config=<CFG>    Path to configuration file (default: ./invoicing.ini)
    --without-logo    No logo in PDF invoice
'''

import argparse
import sys
from importlib.metadata import version
from pathlib import Path

from schwarz.pyinvoice.check import MetaInfo, check_invoice
from schwarz.pyinvoice.config import parse_config
from schwarz.pyinvoice.parser import InvoiceParser
from schwarz.pyinvoice.pdf_generator import generate_pdf, is_weasyprint_available


__all__ = ['cli_main']

def build_parser():
    description = __doc__.splitlines()[0]
    parser = argparse.ArgumentParser(prog='pyinvoice', description=description)
    parser.add_argument('--version', action='version', version=version('pyinvoice'))
    parser.add_argument('--config', metavar='CFG',
                        help='Path to configuration file (default: ./invoicing.ini)')
    parser.add_argument('--without-logo', action='store_true', help='No logo in PDF invoice')
    parser.add_argument('--ignore', metavar='KEY', action='append', default=[],
                        help='Ignore the error with that key (can be used multiple times)')
    parser.add_argument('invoice', metavar='INVOICE', help='XML invoice file')
    parser.add_argument('pdf', metavar='PDF', nargs='?',
                        help='Path of the generated PDF (default: next to the XML file)')
    return parser


def cli_main(argv=None):
    args = build_parser().parse_args(argv)
    path_invoice_xml = args.invoice

    if not Path(path_invoice_xml).exists():
        sys.stderr.write('Invoice file "%s" does not exist.\n' % path_invoice_xml)
        sys.exit(1)
    path_cfg = args.config
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

    ignored_errors = args.ignore
    with_logo = not args.without_logo
    pdf_path = args.pdf
    if not pdf_path:
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


if __name__ == '__main__':
    cli_main()
