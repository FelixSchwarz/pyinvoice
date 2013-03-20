"pyinvoice" is a Python tool to generate invoices using a custom XML format and RML. 

This tool was generated as an ad-hoc solution, the initial code is from 2006 
or so and was actually never intended to be published. Therefore the code-style
is sometimes Java-like.

It was only open-sourced because of requests from members in the 
Python User Group Berlin. However I realize that there are still several 
glitches to make it work nicely on other computers.

Please note: No setup.py yet, please install dependencies manually 
(see "required packages.txt").

Installation:
 - install dependencies manually (see "required packages.txt"), no setup.py yet
 - enter your personal information in userdata/invoicing_data.conf

Usage:
 - add your invoice data in userdata/invoice_data/invoice00001
 - ./generate-invoice 0001

notes:
I'm using a patched pyPdf so I can update PDF attributes (e.g. title) when 
merging two files.

