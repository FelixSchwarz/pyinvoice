#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from invoicegenerator.model.address import Address

class TestAddress(unittest.TestCase):

    def test_equals(self):
        """Test that the custom equals function is working.."""
        a = Address("Foo Bar", "Bridge Street", "01234", "City", ["a", "b"])
        b = Address("Foo Bar", "Bridge Street", "01234", "City", ["a", "b"])
        self.assertEquals(a, a)
        self.assertEquals(a, b)
        self.failUnless( not (a == Address("Bar Foo", "Bridge Street", "01234", "City", ["a", "b"])) )

    def test_inequal(self):
        """Test that the custom ne function is working.."""
        a = Address("Foo Bar", "Bridge Street", "01234", "City", ["a", "b"])
        self.failUnless(not (a != Address("Foo Bar", "Bridge Street", "01234", "City", ["a", "b"])))
        self.failUnless(a != None)
        self.failUnless(a != "invalid")
        self.failUnless(a != Address("Bar Foo", "Bridge Street", "01234", "City", ["a", "b"]))
        self.failUnless(a != Address("Foo Bar", "Tower Street",  "01234", "City", ["a", "b"]))
        self.failUnless(a != Address("Foo Bar", "Bridge Street", "12345", "City", ["a", "b"]))
        self.failUnless(a != Address("Foo Bar", "Bridge Street", "01234", "Village", ["a", "b"]))
        self.failUnless(a != Address("Foo Bar", "Bridge Street", "01234", "City", None))
        self.failUnless(a != Address("Foo Bar", "Bridge Street", "01234", "City", ["c", "d"]))


if __name__ == "__main__":
    unittest.main()
