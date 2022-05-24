# Script to convert csv to IIF output.

import os
import sys, traceback, re
import csv

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

def error(trans):
    sys.stderr.write("%s\n" % trans)
    traceback.print_exc(None, sys.stderr)


input_file_name = sys.argv[1]
invnum = sys.argv[2]
print(input_file_name, invnum)
cust_file = os.path.join(PROJECT_ROOT, 'custs.csv')
customers = {}
product_file = os.path.join(PROJECT_ROOT, 'products.csv')
products = {}
invoice_dir = os.path.join(PROJECT_ROOT, '/invoices/')
trans_date = ""
check_num = 0
curcust = ""
tmpcust = ""
prevcust = ""
trans_type = ""
product = ""
trans_amount = 0

head = "!TRNS	TRNSID	TRNSTYPE	DATE	ACCNT	NAME	CLASS	AMOUNT	DOCNUM	MEMO	CLEAR	TOPRINT	NAMEISTAXABLE	ADDR1	ADDR3	TERMS	SHIPVIA	SHIPDATE\r\n" \
+ "!SPL	SPLID	TRNSTYPE	DATE	ACCNT	NAME	CLASS	AMOUNT	DOCNUM	MEMO	CLEAR	QNTY	PRICE	INVITEM	TAXABLE	OTHER2	YEARTODATE	WAGEBASE\r\n" \
+ "!ENDTRNS\r\n"

template1 = "TRNS		INVOICE	%s	Accounts Receivable	    %s	%s	%s		N	N	N			Due on receipt		%s\r\n"
template2 = "SPL		INVOICE	%s	%s			-%s			N		%s		N		0	0\r\n"
trans_end = "ENDTRNS\r\n"

with open(cust_file, mode='r') as cst_file:
    reader = csv.reader(cst_file)
    for rows in reader:
        if reader.line_num == 1:
            continue
        if rows[0] != "":
            customers.update({rows[0]:rows[1]})
    cst_file.close()

with open(product_file, mode='r') as prd_file:
    reader = csv.reader(prd_file)
    for rows in reader:
        if reader.line_num == 1:
            continue
        if rows[0] != "":
            products.update({rows[0]:rows[1]})
    prd_file.close()

with open(os.path.join(PROJECT_ROOT, input_file_name), mode='r') as our_file:
    reader = csv.reader(our_file)
    for rows in our_file:
        print(rows.line_num)
        if reader.line_num == 1:
            try:
                (check_num, trans_date) = rows
                print(reader.line_num, rows.count)
                assert(rows.count) == 2
            except:
                error(rows)
                continue

        if reader.line_num > 1:
            try:
                assert(rows.count == 3)
            except:
                error(rows)
                continue

        # try:
        #     (curcust, trans_type, trans_amount) = list

        # except:
        #     error(trans)
        #     continue

        # try:
        #     tmpcust = customers.get(curcust)
        #     assert(tmpcust != "")
        # except:
        #     error(trans)
        #     continue

        # try:
        #     product = products.get(trans_type)
        #     assert(product != "")
        # except:
        #     error(trans)
        #     continue

        # if curcust != "" and prevcust =="":
        #     prevcust = curcust
        #     inv_file = open(invoice_dir + 'inv' + invnum + '.iif', mode = 'w')
        #     inv_file.write(head)
        #     inv_file.write(template1 %(trans_date, tmpcust, trans_amount, invnum, trans_date))
        #     continue
        
        # if curcust == prevcust:
        #     inv_file.write(template2 %(trans_date, product, trans_amount, trans_amount))
        #     continue
        
        # if curcust != prevcust and prevcust != "":
        #     inv_file.write(trans_end)
        #     inv_file.close()
        #     invnum += 1
        #     prevcust = ""
        #     continue
