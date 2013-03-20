#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from optparse import OptionParser
import os
import sys

this_dir = os.path.abspath(os.path.dirname(__file__))
libdir = os.path.join(this_dir, "lib")
sys.path.insert(0, libdir)

from invoicegenerator.config import ConfigStore
from invoicegenerator.generator.rml.rmlgenerator import RMLGenerator
from invoicegenerator.parser.lxml.invoiceparser import InvoiceParser

# Requirements for this program:
#    * Python 2.4+ (annotations)
#    * setuptools
#    * lxml

# RML-Generator
#    * genshi
#    * Babel
#    * pyPdf
#    * z3c.rml
#       * zope.interface

def print_usage():
    print 'usage: %s <invoicenumber>' % sys.argv[0]

def invoice_file_name(invoice_number):
    try:
        invoice_number = int(invoice_number)
        return "invoice%05d" % invoice_number
    except ValueError:
        return "invoice-%s" % str(invoice_number)

    
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--with-logo", dest="with_logo", action="store_true", 
                      default=False, help="embed logo in the PDF")
    (options, args) = parser.parse_args()
    
    if args == []:
        print_usage()
        sys.exit(0)
    
    
    user_basedir = "userdata"
    basedir = os.path.join(user_basedir, "output")
    basename = invoice_file_name(args[0])
    
    config_filename = os.path.join(user_basedir, "invoicing_data.conf")
    ConfigStore.read_configuration(config_filename)

    datafile = os.path.join(user_basedir, "invoice_data", basename + ".xml")
    invoice = InvoiceParser.parse(content=file(datafile).read())
    generator = RMLGenerator(invoice)
    generator.build(basedir, basename, options.with_logo)

