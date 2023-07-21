"pyinvoice" is a Python tool to generate PDF invoices using a custom XML format and weasyprint.


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

If the invoice is set to English/USD the rendered string will be "My work: 16.75 h at $60.00".
For German/EUR the output is "My work: 16,75 h at 60,00 €".

