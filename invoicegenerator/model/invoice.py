#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from decimal import Decimal, ROUND_HALF_UP

class Invoice(object):
    DEFAULT_LANGUAGE = "de"
    DEFAULT_CURRENCY = 'EUR'
    
    def __init__(self, invoice_date, billing_address, invoice_items=[], default_vat=0.0, invoice_number="", invoice_subject="", note="", language=DEFAULT_LANGUAGE, currency=DEFAULT_CURRENCY):
        """invoice_date is an arbitrary string representing the invoice date."""
        self.invoice_date = invoice_date
        self.billing_address = billing_address
        self.items = invoice_items
        self.default_vat = Decimal(str(default_vat))
        self.invoice_number = invoice_number
        self.invoice_subject = invoice_subject
        self.note = note
        self.language = language
        self.currency = currency
    
    def get_billing_address(self):
        return self.billing_address

    def get_invoice_items(self):
        return self.items
    
    def get_language(self):
        return self.language
    
    def get_real_sum(self, netto=False):
        """Return the netto sum of all invoice items with all digits after the decimal point."""
        sum = Decimal("0")
        for i in self.items:
            sum += i.get_real_price(netto)
        return sum

    def get_sum(self, netto=False):
        """Return the netto sum of all invoice items with only two digits after the decimal point.
        Brutto sums are calculated as netto sum + vat sum -- even if there would be a different
        result due to rounding if calculating real netto sum * vat."""
        nettosum = self.get_real_sum(netto=True)
        nettosum = nettosum.quantize(Decimal('0.01'), ROUND_HALF_UP)
        if netto:
            return nettosum 
        else:
            vat_sums = self.get_vat_sums()
            vat = Decimal("0")
            for (rate, sum) in vat_sums:
                vat += sum
            return nettosum + vat.quantize(Decimal('0.01'), ROUND_HALF_UP)

    def get_vat_sums(self):
        """Return the sums of item vats by vat rate ordered ascendingly by rate. Sums are limited to
        two digits after the decimal point."""
        vats = self.get_real_vat_sums()
        rounded_vats = []
        for (rate, sum) in vats:
            sum = sum.quantize(Decimal('0.01'), ROUND_HALF_UP)
            rounded_vats.append((rate, sum))
        return rounded_vats

    def get_real_vat_sums(self):
        """Return the sums of item vats by vat rate ordered ascendingly by rate."""
        vats = {}
        for i in self.items:
            rate = i.vat
            if not vats.has_key(rate):
                vats[rate] = Decimal("0")
            vats[rate] += i.get_vat()
        key_list = vats.keys()
        key_list.sort()
        vat_list = []
        for i in key_list:
            vat_list.append((i, vats[i]))
        return vat_list
        
    def __eq__(self, other):
        if other == None or not isinstance(other, Invoice):
            return False
        same_invoice_date = (self.invoice_date == other.invoice_date)
        same_billing_address = (self.billing_address == other.billing_address)
        same_items = (self.items == other.items)
        same_default_vat = (self.default_vat == other.default_vat)
        same_invoice_number = (self.invoice_number == other.invoice_number)
        same_invoice_subject = (self.invoice_subject == other.invoice_subject)
        same_note = (self.note == other.note)
        same_language = (self.language == other.language)
        same_currency = (self.currency == other.currency)
        return (same_invoice_date and same_billing_address and same_items and \
                same_default_vat and same_invoice_number and \
                same_invoice_subject and same_note and same_language and 
                same_currency)

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        text = str(self.get_billing_address()) + "\n"
#        text += str(self.items)
        for i in self.items:
            text += str(i) + "\n"
        return text


