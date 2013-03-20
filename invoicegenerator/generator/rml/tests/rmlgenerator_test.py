# encoding: utf-8

from babel.support import Format
from lxml import etree

from invoicegenerator.config import ConfigStore
from invoicegenerator.generator.rml.rmlgenerator import RMLGenerator
from invoicegenerator.lib.pythonic_testcase import *
from invoicegenerator.model.address import Address
from invoicegenerator.model.invoice import Invoice
from invoicegenerator.model.invoice_item import InvoiceItem

DEFAULT_CONFIG = [
    "[fnord]",
    "name = 'name'", "street = 'street'", "zip = 'zip'", "city = 'city'", "email = 'email'", 
    "tel = 'tel'", "url = 'url'", "ustidnr = 'ustidnr'", "taxnr = 'taxnr'",
    "bank_account_nr = 'bank_account_nr'", "bank_code_nr = 'bank_code_nr'", "bank_name = 'bank_name'",
    "bank_iban = '1234'", "bank_bic = '1234'", 
    "paypal = 'foo@bar.com'",
]

class RMLGeneratorTest(PythonicTestCase):

    def setUp(self):
        self.path_to_template_file = 'invoicegenerator/generator/rml/rg.rml'
        self.lines = DEFAULT_CONFIG + ["rml_template='%s'" % self.path_to_template_file,]
        ConfigStore.read_configuration(self.lines)
        self.billing_address = Address(name="", street="", zipcode="", city="")
        self.invoice = Invoice(invoice_date="19.08.2011", billing_address=self.billing_address)
        self.generator = RMLGenerator(self.invoice)

    def tearDown(self):
        ConfigStore.reset()

    def test_can_instantiate(self):
        assert_equals(self.invoice, self.generator.invoice)
    
    def test_can_render_template(self):
        rendered_rml = self.generator.render_template()
        self.assertTrue(len(rendered_rml) >= 1)
    
    def test_can_count_positions(self):
        item1 = InvoiceItem(name="first", item_price=1)
        item2 = InvoiceItem(name="second", item_price=2)
        self.invoice.items = [item1, item2]
        
        rml_as_xml = self.generator.render_template()
        parsed = etree.fromstring(rml_as_xml)
        # the table has three columns
        first_position = parsed.findall(".//blockTable[@style='position_table']/tr/td")[1 * 3].text
        second_position = parsed.findall(".//blockTable[@style='position_table']/tr/td")[2 * 3].text
        assert_equals(1, int(first_position))
        assert_equals(2, int(second_position))
    
    def test_renders_prices_with_correct_currency(self):
        assert_equals(u'1.024,00 €', self.generator.format_price(1024))
        
        self.generator.invoice.currency = 'USD'
        self.generator.format = Format(locale='en')
        assert_equals('en', str(self.generator.format.locale))
        assert_equals(u'$1,024.00', self.generator.format_price(1024))

