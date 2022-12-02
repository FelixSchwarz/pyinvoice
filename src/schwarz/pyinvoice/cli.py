'''Generate PDF invoices from XML files.

Usage:
    pyinvoice [options] <INVOICE> [<PDF>]

Arguments:
    --config=<CFG>    Path to configuration file (default: ./invoicing.ini)
    --with-logo       Include logo in PDF invoice
'''

from pathlib import Path
import sys

from argopt import argopt

from .config import parse_config
from .parser import InvoiceParser
from .pdf_generator import generate_pdf


__all__ = ['cli_main']

def cli_main():
    args = argopt(__doc__).parse_args()
    path_invoice_xml = args.INVOICE
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

    with_logo = args.with_logo
    # == 'None' because argopt 0.7.1 uses that in case the user did not specify
    # the value explicitely
    if (not args.PDF) or (args.PDF == 'None'):
        suffix = ('.logo' if with_logo else '') + '.pdf'
        pdf_path = Path(path_invoice_xml).with_suffix(suffix)
    else:
        pdf_path = Path(args.PDF)
    if pdf_path.exists():
        sys.stderr.write('PDF "%s" already exists, will not overwrite existing file.\n' % str(pdf_path))
        sys.exit(2)

    invoice = InvoiceParser.parse(filename=path_invoice_xml)
    invoice_cfg = parse_config(path_cfg)
    generate_pdf(invoice, invoice_cfg, target_path=pdf_path, with_logo=with_logo)

