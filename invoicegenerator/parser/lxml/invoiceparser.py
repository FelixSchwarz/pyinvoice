#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from decimal import Decimal
from StringIO import StringIO

from lxml import etree
from pkg_resources import resource_string

from invoicegenerator.model.invoice import Invoice

from invoicegenerator.parser.lxml.addressparser import AddressParser
from invoicegenerator.parser.lxml.invoiceitemparser import InvoiceItemParser

class InvoiceParser(object):
    @classmethod
    def get_valid_xml(cls, filename=None, content=None):
        contents = resource_string("invoicegenerator.xmlschema", 'invoice_document.xsd')
        xmlschema_doc = etree.parse(StringIO(contents))
        xmlschema = etree.XMLSchema(xmlschema_doc)
        if content == None:
            content = file(filename).read()
        doc = etree.parse(StringIO(content))
        
        xmlschema.assertValid(doc)
        return doc
    
    @classmethod
    def _parse_attributes(cls, element):
        (subject, date, number, default_vat, language) = ("", "", "", Decimal("0.0"), Invoice.DEFAULT_LANGUAGE)
        currency = Invoice.DEFAULT_CURRENCY
        attributes = element.attrib
        if attributes.has_key("invoiceSubject"):
            subject = attributes["invoiceSubject"]
        if attributes.has_key("invoiceDate"):
            date = attributes["invoiceDate"]
        if attributes.has_key("invoiceNumber"):
            number = attributes["invoiceNumber"]
        if attributes.has_key("defaultVat"):
            default_vat = Decimal(attributes["defaultVat"])
        if attributes.has_key("language"):
            language = attributes["language"]
        if attributes.has_key('currency'):
            currency = attributes['currency']
        return (subject, date, number, default_vat, language, currency)
    
    @classmethod
    def parse(cls, content=None, filename=None):
        doc = cls.get_valid_xml(content=content, filename=filename)
        root = doc.getroot()
        (subject, date, number, default_vat, language, currency) = cls._parse_attributes(root)
        address, items, note = None, [], None
        for item in root.getchildren():
            if item.tag == "billingAddress":
                address = AddressParser.parse_element(item)
            elif item.tag == "item":
                items.append(InvoiceItemParser.parse_element(item, default_vat=default_vat))
            elif item.tag == "note":
                note = item.text
        return Invoice(date, address, items, default_vat=default_vat, 
                       invoice_number=number, invoice_subject=subject, 
                       note=note, language=language, currency=currency)
