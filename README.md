"pyinvoice" is a Python tool to generate PDF invoices using a custom XML format and [WeasyPrint](https://weasyprint.org/).

## Usage

pyinvoice is a command line tool which is really simple to use:

```shell
$ pyinvoice my-invoice.xml
```

Afterwards you should find a PDF file `my-invoice.pdf` right next to the xml file.
Before using pyinvoice for the first time you need to setup/configure some things.

## Installation/Setup

### Installation

TDB

### Create a HTML template for WeasyPrint

TDB

### Create a configuration file

pyinvoice uses a simple configuration file to store information about the invoice issuer.
That way you can use a single invoice template for different businesses.

If the configuration file is named `invoicing.ini` in the working directory where you called
pyinvoce the file will be picked up automatically. Otherwise you need to specify the config
file explicitely using `--config=/path/to/invoicing.ini`.

Example config:

```
[pyinvoice]
name      = John Smith
street    = Main Street 54
zip       = 80331
city      = Munich
tel       = (089) 123456
email     = john@site.example
domain    = www.site.example

ustidnr   = DE123456789
taxnr     = 11/555/00123

bank_iban = DE12 1001 0010 0123 4567 89
bank_bic  = PBNKDEFF
bank_name = Postbank
paypal    = john@site.example

template  = ./templates/invoice.html
```

Which data you put in there is up to you and the template you use. The only required key is
`template` which pyinvoice uses to load the right HTML template.


---

## Create an Invoice

To create an invoice you need to create an XML file with the right information. pyinvoice will calculate the
net sum, VAT values and the total sum automatically for you.

```xml
<?xml version="1.0" encoding='UTF-8'?>
<invoice invoiceSubject="Software to create PDF Invoices"
         invoiceDate="21.07.2023" invoiceNumber="00213"
         defaultVat="0.19">

	<billingAddress>
	   <name>Customer Ltd</name>
	   <street>Business Street 2</street>
	   <zip>10715</zip>
	   <city>Berlin</city>
	</billingAddress>

	<item price="230">
		Development of software to create PDF invoices
	</item>
</invoice>
```

You can use multiple invoice `<item>` elements inside a single invoice. pyinvoice will sum the prices
for all positions automatically.


---

## Advanced Topics

### Custom check functions

TDB


### Item price calculation based on `hours` and `hourly_rate`

pyinvoice can calculate an item price using hours and an hourly rate.
This can be helpful for freelancers who want to create an invoice based on the
number of hours worked.

**Example:**

```xml
<item hours="16.75" hourly_rate="60">
    My work
</item>
```

When generating the PDF pyinvoice will calculate the price as 16.75 * 60 = 1005.


### Templating

Optionally you can use `hours` and `hourly_rate` in the item description to avoid inconsistencies
and duplicate information. pyinvoice will apply number formatting (according to the invoice
language) for all numbers automatically. `|amount` means the value represents an amount so it
will be rendered as a currency value.

**Example:**

```xml
<item hours="16.75" hourly_rate="60">
    My work: {hours} h at {hourly_rate|amount}
</item>
```

To apply templating you need to call the `tt()` template function in your html template, for example like this:

```html
{% for item in invoice.get_invoice_items() %}
<tr class="position-row">
    <td>
        {% if item.get_title() %}
        <div class="pos-title">{{ tt(item.get_title(), item) }}</div>
        {% endif %}
        {{ tt(item.get_subtext(), item) }}
    </td>
    <td class="net-amount">
        {{ f.amount(item.get_price(net=True)) }}
    </td>
</tr>
{% endfor %}
```

If the invoice is set to English/USD the rendered string will be "My work: 16.75 h at $60.00".
For German/EUR the output is "My work: 16,75 h at 60,00 €".

