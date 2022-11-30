# -*- coding: UTF-8 -*-


from ..address import Address

def test_address_equals():
    a = Address('Foo Bar', 'Bridge Street', '01234', 'City', ['a', 'b'])
    b = Address('Foo Bar', 'Bridge Street', '01234', 'City', ['a', 'b'])
    assert a == a
    assert b == b
    other = Address('Bar Foo', 'Bridge Street', '01234', 'City', ['a', 'b'])
    assert not (a == other)

def test_address_inequal():
    """Test that the custom ne function is working.."""
    a = Address('Foo Bar', 'Bridge Street', '01234', 'City', ['a', 'b'])
    assert not (a != Address('Foo Bar', 'Bridge Street', '01234', 'City', ['a', 'b']))
    assert a != None
    assert a != 'invalid'
    assert a != Address('Bar Foo', 'Bridge Street', '01234', 'City', ['a', 'b'])
    assert a != Address('Foo Bar', 'Tower Street',  '01234', 'City', ['a', 'b'])
    assert a != Address('Foo Bar', 'Bridge Street', '12345', 'City', ['a', 'b'])
    assert a != Address('Foo Bar', 'Bridge Street', '01234', 'Village', ['a', 'b'])
    assert a != Address('Foo Bar', 'Bridge Street', '01234', 'City', None)
    assert a != Address('Foo Bar', 'Bridge Street', '01234', 'City', ['c', 'd'])

