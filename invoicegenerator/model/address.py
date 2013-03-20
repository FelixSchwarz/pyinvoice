#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class Address(object):
    def __init__(self, name, street, zipcode, city, additional_lines=[]):
        self.name = name
        self.street = street
        self.zipcode = zipcode
        self.city = city
        self.additional_lines = additional_lines
        
    def __eq__(self, other):
        if other == None or not isinstance(other, Address):
            return False
        same_name = (self.name == other.name)
        same_street = (self.street == other.street)
        same_zip = (self.zipcode == other.zipcode)
        same_city = (self.city == other.city)
        same_additional = (self.additional_lines == other.additional_lines)
        return same_name and same_street and same_zip and same_city and same_additional

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        additional = ''
        if self.additional_lines != None and self.additional_lines != []:
            additional = "\n".join(self.additional_lines + [''])
        return self.name + "\n" + additional + \
                           self.street + "\n" + self.zipcode + " " + self.city


