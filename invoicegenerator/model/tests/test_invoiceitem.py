#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from decimal import Decimal
import unittest

from invoicegenerator.model.invoice_item import InvoiceItem

class TestInvoiceItem(unittest.TestCase):

    def test_get_real_price(self):
        """Test that Decimal computation is used."""
        item = InvoiceItem("foo", 2.333, number=2)
        self.assertEquals(Decimal("4.666"), item.get_real_price())

    def test_get_price(self):
        """Test that prices have only two digits after the decimal point."""
        item = InvoiceItem("foo", 2.333, number=2)
        self.assertEquals(Decimal("4.67"), item.get_price())
        
        item = InvoiceItem("foo", 2.333, number=2, vat=0.5)
        self.assertEquals(Decimal("4.67"), item.get_price(netto=True))

    def test_get_real_price_vat(self):
        """Test that vat is added correctly."""
        item = InvoiceItem("foo", 10, vat=0.10)
        self.assertEquals(Decimal("11"), item.get_real_price())
        self.assertEquals(Decimal("10"), item.get_real_price(netto=True))

        item = InvoiceItem("foo", 10, vat=0.50)
        self.assertEquals(Decimal("15"), item.get_real_price())
        self.assertEquals(Decimal("10"), item.get_real_price(netto=True))

    def test_get_vat(self):
        """Test that vat is computed correctly."""
        item = InvoiceItem("foo", 1, vat=0.10, number=10)
        self.assertEquals(Decimal("1"), item.get_vat())


    def test_equals(self):
        """Test that the custom equals function is working.."""
        a = InvoiceItem("foo", 10, vat=0.10, number=2)
        b = InvoiceItem("foo", 10, vat=0.10, number=2)
        self.assertEquals(a, a)
        self.assertEquals(a, b)
        self.failUnless( not (a == InvoiceItem("bar", 10, vat=0.10, number=2)) )

    def test_inequal(self):
        """Test that the custom ne function is working.."""
        a = InvoiceItem("foo", 10, vat=0.10, number=2)
        self.failUnless(not (a != InvoiceItem("foo", 10, vat=0.10, number=2)))
        self.failUnless(a != None)
        self.failUnless(a != "invalid")
        self.failUnless(a != InvoiceItem("bar", 10, vat=0.10, number=2))
        self.failUnless(a != InvoiceItem("foo", 15, vat=0.10, number=2))
        self.failUnless(a != InvoiceItem("foo", 10, vat=0.20, number=2))
        self.failUnless(a != InvoiceItem("foo", 10, vat=0.10, number=4))



if __name__ == "__main__":
    unittest.main()
