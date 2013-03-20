#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from decimal import Decimal

class InvoiceItem(object):
    def __init__(self, name, item_price, vat=0, number=1):
        self.name = name
        self.number = Decimal(str(number))
        self.item_price = Decimal(str(item_price))
        self.vat = Decimal(str(vat))
    
    def _compute_vat(self, price, vat):
        return price * vat

    def get_vat(self):
        return self.number * self._compute_vat(self.item_price, self.vat)
        
    def get_price(self, netto=False):
        """Return the price with only two digits after the decimal point."""
        price = self.get_real_price(netto)
        return price.quantize(Decimal('0.01'))

    def get_real_price(self, netto=False):
        """Return the price with all digits after the decimal point."""
        price = self.number * self.item_price
        if not netto:
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
