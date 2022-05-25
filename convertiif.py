# Script to convert csv to IIF output.

import os
import sys, traceback, re
import csv

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

def error(trans):
    sys.stderr.write("%s\n" % trans)
    traceback.print_exc(None, sys.stderr)


input_file_name = sys.argv[1]
invnum = int(sys.argv[2])
cust_file = os.path.join(PROJECT_ROOT, 'custs.csv')
product_file = os.path.join(PROJECT_ROOT, 'products.csv')
invoice_dir = os.path.join(PROJECT_ROOT, 'invoices/')
customers = dict()
products = dict()
transactions = list()
current_trans = list()
customer = ""
tmp_cust = ""
total_amount = 0
trans_date = ""

head = "!TRNS	TRNSID	TRNSTYPE	DATE	ACCNT	NAME	CLASS	AMOUNT	DOCNUM	MEMO	CLEAR	TOPRINT	NAMEISTAXABLE	ADDR1	ADDR3	TERMS	SHIPVIA	SHIPDATE\r\n" \
+ "!SPL	SPLID	TRNSTYPE	DATE	ACCNT	NAME	CLASS	AMOUNT	DOCNUM	MEMO	CLEAR	QNTY	PRICE	INVITEM	TAXABLE	OTHER2	YEARTODATE	WAGEBASE\r\n" \
+ "!ENDTRNS\r\n"

template1 = "TRNS		INVOICE	%s	Accounts Receivable	    %s	%s	%s		N	N	N			Due on receipt		%s\r\n"
template2 = "SPL		INVOICE	%s	%s			-%s			N		%s		N		0	0\r\n"
trans_end = "ENDTRNS\r\n"

with open(cust_file, mode='r') as cst_file:
    reader = csv.reader(cst_file)
    for row in reader:
        if reader.line_num == 1:
            continue
        customers.update({row[0]:row[1]})
    cst_file.close()

with open(product_file, mode='r') as prd_file:
    reader = csv.reader(prd_file)
    for row in reader:
        if reader.line_num == 1:
            continue
        products.update({row[0]:row[1]})
    prd_file.close()

with open(os.path.join(PROJECT_ROOT, input_file_name), mode='r') as our_file:
    transactions = list(csv.reader(our_file))
    our_file.close()

for row in range(len(transactions)):
    if row == 0:
        continue

    current_trans = transactions[row]
    tmp_cust = current_trans[0]
    if tmp_cust != "":
        customer = customers.get(tmp_cust, "")
        if customer == "":
            error(tmp_cust)
            exit(1)
        else:
            total_amount += float(current_trans[2])
            

    # reader = csv.reader(our_file)
    # for rows in reader:
    #     if reader.line_num == 1:
    #         continue

    #     if reader.line_num == 2:
    #         try:
    #             check_num = int(rows[0])
    #             trans_date = rows[1]
    #             assert(rows[0] != 0)
    #         except:
    #             error(rows)
    #             continue

    #     if reader.line_num > 2:
    #         try:
    #             curcust = rows[0]
    #             trans_type = rows[1]
    #             trans_amount = float(rows[2])
    #             assert(curcust != "" and trans_type != "" and trans_amount != 0)
    #         except:
    #             error(rows)
    #             continue

    #         try:
    #             trans_cust = customers.get(curcust)
    #             assert(trans_cust != "")
    #         except:
    #             error(rows)
    #             continue

    #         try:
    #             product = products.get(trans_type)
    #             assert(product != "")
    #         except:
    #             error(rows)
    #             continue

    #         if curcust != "" and prevcust =="":
    #             prevcust = curcust
    #             inv_file = open(invoice_dir + 'inv' + str(invnum) + '.iif', mode = 'w')
    #             inv_file.write(head)
    #             inv_file.write(template1 %(trans_date, trans_cust, trans_amount, invnum, trans_date))
    #             inv_file.write(template2 %(trans_date, product, trans_amount, trans_amount))
    #             continue
            
    #         if curcust == prevcust:
    #             inv_file.write(template2 %(trans_date, product, trans_amount, trans_amount))
    #             continue
            
    #         if curcust != prevcust and prevcust != "":
    #             inv_file.write(trans_end)
    #             inv_file.close()
    #             invnum += 1
    #             prevcust = ""
    #             continue
