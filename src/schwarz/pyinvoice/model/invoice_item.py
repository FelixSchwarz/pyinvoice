# -*- coding: UTF-8 -*-

from decimal import Decimal
import re


__all__ = ['InvoiceItem']

class InvoiceItem:
    def __init__(self, name, item_price, vat=0, number=1):
        self.name = name
        self.number = Decimal(str(number))
        self.item_price = Decimal(str(item_price))
        self.vat = Decimal(str(vat))

    def _compute_vat(self, price, vat):
        return price * vat

    def get_title(self):
        pos_title, _ = self._split_title_and_subtext()
        return pos_title

    def get_subtext(self):
        _, pos_subtext = self._split_title_and_subtext()
        return pos_subtext

    def _split_title_and_subtext(self):
        if '//' not in self.name:
            return (None, self.name)
        m = re.search(r'^(.+?)\s*//\s*(.+?)$', self.name)
        pos_title, pos_subtext = m.groups()
        return (pos_title, pos_subtext)

    def get_vat(self):
        return self.number * self._compute_vat(self.item_price, self.vat)

    def get_price(self, net=False):
        """Return the price with only two digits after the decimal point."""
        price = self.get_real_price(net)
        return price.quantize(Decimal('0.01'))

    def get_real_price(self, net=False):
        """Return the price with all digits after the decimal point."""
        price = self.number * self.item_price
        if not net:
            price += self._compute_vat(price, self.vat)
        return Decimal(str(price))

    def __eq__(self, other):
        if other == None or not isinstance(other, InvoiceItem):
            return False
        same_name = (self.name == other.name)
        same_price = (self.item_price == other.item_price)
        same_vat = (self.vat == other.vat)
        same_number = (self.number == other.number)
        return same_name and same_price and same_vat and same_number

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return self.name + ", " + str(self.number) + ", " + str(self.item_price) + \
                           ", " + str(self.vat)
