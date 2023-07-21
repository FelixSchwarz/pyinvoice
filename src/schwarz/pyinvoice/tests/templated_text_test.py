#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from decimal import Decimal

from schwarz.pyinvoice.model import InvoiceItem
from ..pdf_generator import build_formatter
from ..templating import templated_text


def test_can_return_text_without_templating():
    item = InvoiceItem('foo', item_price=2)
    f = build_formatter('de', currency='EUR')
    assert templated_text('foo bar', item, f) == 'foo bar'

def test_text_with_simple_number_formatting():
    item = InvoiceItem('foo', item_price=2, meta={'hours': Decimal('7.5')})
    f_de = build_formatter('de', currency='EUR')
    assert templated_text('foo: {hours}h', item, f_de) == 'foo: 7,5h'
    f_en = build_formatter('en', currency='EUR')
    assert templated_text('foo: {hours}h', item, f_en) == 'foo: 7.5h'

def test_text_with_amount_formatting():
    item = InvoiceItem('foo', item_price=2, meta={'rate': Decimal('1234.5')})
    f_de = build_formatter('de', currency='EUR')
    assert templated_text('foo: {rate}', item, f_de) == 'foo: 1.234,5'
    assert templated_text('foo: {rate|amount}', item, f_de) == 'foo: 1.234,50\xa0€'
    f_en_usd = build_formatter('en', currency='USD')
    assert templated_text('foo: {rate|amount}', item, f_en_usd) == 'foo: $1,234.50'

def test_with_multiple_templated_parts():
    m = {'hours': Decimal('7.5'), 'rate': Decimal('12.3')}
    item = InvoiceItem('foo', item_price=2, meta=m)
    f_de = build_formatter('de', currency='EUR')
    assert templated_text('foo: {rate} / {hours}h', item, f_de) == 'foo: 12,3 / 7,5h'
    assert templated_text('foo: {rate|amount} / {hours}h', item, f_de) == 'foo: 12,30\xa0€ / 7,5h'
