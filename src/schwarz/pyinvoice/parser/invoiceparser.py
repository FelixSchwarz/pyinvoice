# -*- coding: UTF-8 -*-

from datetime import date as Date
from decimal import Decimal
import importlib.resources
from io import BytesIO, StringIO
import re

from lxml import etree

from ..model.invoice import Invoice
from .addressparser import AddressParser
from .invoiceitemparser import InvoiceItemParser


__all__ = ['InvoiceParser']

class InvoiceParser(object):
    @classmethod
    def _invoice_schema(cls):
        xsd_ref = importlib.resources.files('schwarz.pyinvoice.parser.xmlschema').joinpath('Invoice.xsd')
        with xsd_ref.open('r', encoding='utf8') as xsd_fp:
            xml_parser = etree.XMLParser(load_dtd=True)
            xmlschema_doc = etree.parse(xsd_fp, xml_parser)
        xml_schema = etree.XMLSchema(xmlschema_doc)
        return xml_schema

    @classmethod
    def get_valid_xml(cls, filename=None, content=None):
        xmlschema = cls._invoice_schema()
        if content is None:
            content_fp = open(filename, 'rb')
        elif isinstance(content, bytes):
            content_fp = BytesIO(content)
        elif isinstance(content, str):
            content_fp = StringIO(content)
        else:
            raise NotImplementedError()
        doc = etree.parse(content_fp)
        xmlschema.assertValid(doc)
        if hasattr(content_fp, 'close'):
            content_fp.close()
        return doc

    @classmethod
    def _parse_attributes(cls, element):
        (subject, date, number, default_vat, language) = ('', '', '', Decimal('0.0'), Invoice.DEFAULT_LANGUAGE)
        currency = Invoice.DEFAULT_CURRENCY
        attributes = element.attrib
        if attributes.has_key('invoiceSubject'):
            subject = attributes['invoiceSubject']
        if attributes.has_key('invoiceDate'):
            date_str = attributes['invoiceDate']
            m_date = re.search(r'^(\d{4})\-(\d{2})\-(\d{2})$', date_str)
            date = Date(*map(int, m_date.groups())) if m_date else date_str
        if attributes.has_key('invoiceNumber'):
            number = attributes['invoiceNumber']
        if attributes.has_key('defaultVat'):
            default_vat = Decimal(attributes['defaultVat'])
        if attributes.has_key('language'):
            language = attributes['language']
        if attributes.has_key('currency'):
            currency = attributes['currency']
        return (subject, date, number, default_vat, language, currency)

    @classmethod
    def parse(cls, content=None, filename=None):
        if content and not isinstance(content, str):
            content = bytes(content)
        doc = cls.get_valid_xml(content=content, filename=filename)
        root = doc.getroot()
        (subject, date, number, default_vat, language, currency) = cls._parse_attributes(root)
        address, items, note = None, [], None
        for item in root.getchildren():
            if item.tag == 'billingAddress':
                address = AddressParser.parse_element(item)
            elif item.tag == 'item':
                items.append(InvoiceItemParser.parse_element(item, default_vat=default_vat))
            elif item.tag == 'note':
                note = item.text
        return Invoice(date, address, items, default_vat=default_vat, 
                       invoice_number=number, invoice_subject=subject, 
                       note=note, language=language, currency=currency)
