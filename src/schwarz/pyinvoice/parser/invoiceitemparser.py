# -*- coding: UTF-8 -*-

from decimal import Decimal
from io import StringIO

from lxml import etree

from ..model import InvoiceItem

DEFAULT_VAT = 0.0


class InvoiceItemParser(object):
    @classmethod
    def parse_element(self, element, default_vat=DEFAULT_VAT):
        price = None
        number = 1
        vat = default_vat
        meta = {}

        name = element.text.strip()
        attributes = element.attrib
        if attributes.has_key("price"):
            price = attributes["price"]
        if attributes.has_key("number"):
            number = attributes["number"]
        if attributes.has_key("vat"):
            vat = attributes["vat"]

        for key in ('hours', 'hourly_rate'):
            if attributes.has_key(key):
                meta[key] = Decimal(attributes[key])
        if price is None:
            price = meta['hours'] * meta['hourly_rate']
        return InvoiceItem(name, price, number=number, vat=vat, meta=meta)

    @classmethod
    def parse(self, content="", default_vat=DEFAULT_VAT):
        """Parse an InvoiceItem without validation """
        doc = etree.parse(StringIO(content))
        return self.parse_element(doc.getroot(), default_vat)
