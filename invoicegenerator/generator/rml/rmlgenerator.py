# -*- coding: UTF-8 -*-

import os
import re

from babel.support import Format, Translations
from genshi.filters import Translator
from genshi.template import TemplateLoader

from invoicegenerator.config import ConfigStore
from invoicegenerator.generator.rml.lib_rml2pdf import rml_to_pdf, register_fonts_for_language


this_dir = os.path.abspath(os.path.dirname(__file__))

class RMLGenerator(object):
    def __init__(self, invoice):
        self.invoice = invoice
        self.invoice_datetime = ConfigStore.parse_date(self.invoice.invoice_date)
        self.config = ConfigStore.get_configuration(when=self.invoice_datetime)
        
        self.translation = Translations.load('locale', locales=[self.invoice.language], domain='pyinvoice')
        self.ugettext = self.translation.ugettext
        self.format = Format(locale=self.invoice.language)
    
    def build(self, output_dir, basename, should_embed_logo=False):
        rml_string = self.render_template()
        #self.save_rml_file(rml_string, output_dir, basename)
        self.build_pdf(rml_string, output_dir, basename, should_embed_logo)
    
    def render_template(self):
        user_template = self.config['rml_template']
        if os.path.isfile(user_template):
            user_template = os.path.dirname(user_template)
        def template_loaded(template):
            Translator(self.translation).setup(template)
        loader = TemplateLoader([user_template, this_dir], callback=template_loaded)
        
        template = loader.load('rg.rml')
        stream = template.generate(**self.template_variables())
        return stream.render('xhtml')
    
    def build_pdf(self, rml_string, output_dir, basename, should_embed_logo):
        filename = self.get_pdf_filename(output_dir, basename)
        cur_dirname = os.path.dirname(__file__)
        fontdir = os.path.abspath(os.path.join(cur_dirname, "fonts"))
        register_fonts_for_language(self.invoice.language, fontdir)
        pdf_logo_fp = rml_to_pdf(rml_string, embed_logo=should_embed_logo)
        file_handle = file(filename, "wb")
        file_handle.write(pdf_logo_fp.getvalue())
        file_handle.close()

    def save_rml_file(self, rml_string, output_dir, basename):
        filename = self.get_rml_filename(output_dir, basename)
        if isinstance(rml_string, unicode):
            rml_string = rml_string.encode("UTF-8")
        file_handle = file(filename, "w")
        file_handle.write(rml_string)
        file_handle.close()

    def get_rml_filename(self, output_dir, basename):
        filename = os.path.join(output_dir, "%s.%s.rml" % (basename, self.invoice.language))
        return filename

    def get_pdf_filename(self, output_dir, basename):
        filename = os.path.join(output_dir, "%s.%s.pdf" % (basename, self.invoice.language))
        return filename

    def invoicing_party_variables(self):
        return dict(
            name = self.config["name"],
            email = self.config["email"],
            phone = self.config["tel"],
            url = u"http://" + self.config["url"],
            domain = self.config["url"],
            
            bank = dict(
                account_nr = self.config["bank_account_nr"],
                code_nr = self.config["bank_code_nr"],
                name = self.config["bank_name"],
                iban = self.config["bank_iban"],
                bic = self.config["bank_bic"],
            ),
            paypal = self.config["paypal"],
            
            ustidnr = self.config["ustidnr"],
            taxnr = self.config['taxnr'],
            
            address = dict(
                street = self.config["street"],
                zip = self.config["zip"],
                city = self.config["city"],
            ),
        )
    
    def pdf_title(self):
        title_template = self.ugettext("Rechnung Nr. %(number)s vom %(date)s: %(subject)s")
        title_parameters = dict(
            number=self.invoice.invoice_number, 
            date=self.format.date(self.invoice_datetime), 
            subject=self.invoice.invoice_subject
        )
        return title_template % title_parameters
    
    def remove_latex_codes(self, text):
        output = re.sub('\\\-', "", text)
        return output
    
    def text_transform(self, text):
        output = text
        output = re.sub('"(,|\.|\s+)', u"“\\1", output)
        output = re.sub(u'(\s+)"', u'\\1„', output)
        return output
    
    def invoice_item_variables(self):
        items = []
        for i, item in enumerate(self.invoice.get_invoice_items()):
            items.append(dict(
                position = i+1,
                description = self.text_transform(self.remove_latex_codes(item.name)),
                price = self.format_price(item.get_price(netto=True)),
            ))
        return items
    
    def template_variables(self):
        vat_percentage = [0][0]
        return dict(
            title = self.pdf_title(),
            author = self.config["name"],
            invoicing_party = self.invoicing_party_variables(),
            invoice = self.invoice,
            invoice_date = self.format.date(self.invoice_datetime),
            vat_percentage = self.format.percent(vat_percentage),
            
            invoice_items = self.invoice_item_variables(),
            vat_items = self.invoice.get_vat_sums(),
            
            format = self.format,
            format_price = self.format_price,
        )
    
    def format_price(self, price):
        return self.format.currency(price, currency=self.invoice.currency)
