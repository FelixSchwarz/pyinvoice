#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from StringIO import StringIO

from lxml import etree

from invoicegenerator.model.address import Address

class AddressParser(object):
    @classmethod
    def parse_element(self, element):
        (name, street, zipcode, city, additional) = (None, None, None, None, [])
        for item in element.getchildren():
            if item.tag == "name":
                name = item.text
            elif item.tag == "nameDetail":
                additional.append(item.text)
            elif item.tag == "street":
                street = item.text
            elif item.tag == "zip":
                zipcode = item.text
            elif item.tag == "city":
                city = item.text
        return Address(name, street, zipcode, city, additional)
        
    @classmethod
    def parse(self, content=""):
        """Parse an Address without validation """
        doc = etree.parse(StringIO(content))
        return self.parse_element(doc.getroot())
