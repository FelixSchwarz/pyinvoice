# -*- coding: UTF-8 -*-

from schwarz.pyinvoice.model import Address
from ..addressparser import AddressParser


def test_parse_address():
    xml = """<billingAddress>
        <name>FooBar Inc.</name>
        <street>9th Avenue</street>
        <zip>12345</zip>
        <city>New York</city>
    </billingAddress>"""
    address = Address('FooBar Inc.', '9th Avenue', '12345', 'New York', [])
    assert address == AddressParser.parse(content=xml)

