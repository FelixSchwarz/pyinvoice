
import os
from StringIO import StringIO

from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from z3c.rml import rml2pdf
from pyPdf import PdfFileWriter, PdfFileReader

def _get_registered_ttfont(fontinfo, fontdir, default=None):
    if fontinfo != None:
        fontname, ttf_filename = fontinfo
        ttf_filename = os.path.join(fontdir, ttf_filename)
        font = TTFont(fontname, ttf_filename, "UTF-8")
        pdfmetrics.registerFont(font)
        return font
    assert default != None
    return default
    

def register_fontfamily(familyname, fontdir, regular, bold=None, italic=None, 
                        bolditalic=None):
    regular_font = _get_registered_ttfont(regular, fontdir)
    bold_font = _get_registered_ttfont(bold, fontdir, default=regular_font)
    italic_font = _get_registered_ttfont(italic, fontdir, default=regular_font)
    fallback_bold_italic = bold_font or italic_font
    bolditalic_font = _get_registered_ttfont(bolditalic, fontdir, 
                                             default=fallback_bold_italic)
    
    # Mapping must be done after registering all fonts of the same family with
    # pdfmetrics.registerFont because that method will add mappings for all 
    # type faces (this may override previous mappings!).
    map_font(familyname, regular_font, bold=False, italic=False)
    map_font(familyname, bold_font, bold=True, italic=False)
    map_font(familyname, italic_font, bold=False, italic=True)
    map_font(familyname, bolditalic_font, bold=True, italic=True)


def map_font(familyname, font,  bold=False, italic=False):
    assert font._multiByte
    if bold:
        bold = 1
    else:
        bold = 0
    if italic:
        italic = 1
    else:
        italic = 0
    addMapping(familyname, bold, italic, font.fontName)


def monkey_patch_preamble():
    """Patching Canvas._make_preamble so that the font name 'Helvetica' won't 
    be included in output document. This is because it is not possible to embed
    this font into the generated pdf due to internal reportlabs restrictions.
    This workaround was proposed by Robin Becker (8/2004)
    http://two.pairlist.net/pipermail/reportlab-users/2004-August/003268.html"""
    from reportlab.pdfgen import canvas
    def new_make_preamble(self):
        self._preamble = ""
    canvas.Canvas._make_preamble = new_make_preamble


monkey_patch_preamble()


def perform_logo_embedding(pdf_fp, logo_template_fp):
    pdf_fp.seek(0)
    rg_input = PdfFileReader(pdf_fp)

    doc_info = rg_input.getDocumentInfo()
    creator_info = doc_info.creator or doc_info.producer
    final_rg = PdfFileWriter(author=doc_info.author, title=doc_info.title, 
                             subject=doc_info.subject, creator=creator_info)
    
    for page_number in range(rg_input.getNumPages()):
        page = rg_input.getPage(page_number)
        if page_number == 0:
            watermark = PdfFileReader(logo_template_fp)
            page.mergePage(watermark.getPage(0))        
        final_rg.addPage(page)

    pdf_logo_fp = StringIO()
    
    final_rg.write(pdf_logo_fp)    
    pdf_logo_fp.seek(0)
    return pdf_logo_fp


def rml_to_pdf(rml_string, embed_logo=True):
    pdf_fp = rml2pdf.parseString(rml_string)
    
    if embed_logo:
        cur_dirname = os.path.dirname(__file__)
        logo_pdf = os.path.abspath(os.path.join(cur_dirname, "Logo auf A4.pdf"))
        logo_template_fp = file(logo_pdf, "rb")
        pdf_fp = perform_logo_embedding(pdf_fp, logo_template_fp)
    return pdf_fp

def register_fonts_for_language(language, fontdir):
    font_config = dict(
        de={
            "Sans": (
                ("Sans", "AndBasR_tt.ttf"), # Andika Basic Regular
                ("DejaVu Sans Bold", "DejaVuSans-Bold.ttf"),
            ),
            "Gentium": (
                ("Gentium", "GenBasR.ttf"), # Gentium Basic Regular
                ("Gentium Basic Bold", "GenBasB.ttf"),
            ),
        }, en={
            "Sans": (
                ("Sans", "DejaVuSans.ttf"),
                ("DejaVu Sans Bold", "DejaVuSans-Bold.ttf"),
            ),
            "Gentium": (
                ("Gentium", "GenBasR.ttf"), # Gentium Basic Regular
                ("Gentium Basic Bold", "GenBasB.ttf"),
            ),
        },
    )
    fonts_for_language = font_config[language]
    for font_style, fonts in fonts_for_language.iteritems():
        register_fontfamily(font_style, fontdir, *fonts)
    
