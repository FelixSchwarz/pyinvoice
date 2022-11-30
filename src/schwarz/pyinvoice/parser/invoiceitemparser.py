# -*- coding: UTF-8 -*-

from io import StringIO

from lxml import etree

from ..model import InvoiceItem

DEFAULT_VAT = 0.0


class InvoiceItemParser(object):
    @classmethod
    def parse_element(self, element, default_vat=DEFAULT_VAT):
        (price, number, vat) = (0, 1, default_vat)
        name = element.text.strip()
        attributes = element.attrib
        if attributes.has_key("price"):
            price = attributes["price"]
        if attributes.has_key("number"):
            number = attributes["number"]
        if attributes.has_key("vat"):
            vat = attributes["vat"]
        return InvoiceItem(name, price, number=number, vat=vat)

    @classmethod
    def parse(self, content="", default_vat=DEFAULT_VAT):
        """Parse an InvoiceItem without validation """
        doc = etree.parse(StringIO(content))
        return self.parse_element(doc.getroot(), default_vat)
