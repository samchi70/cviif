# Script to convert csv to IIF output.

import os
import sys, traceback, re
import csv

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

def error(trans):
    sys.stderr.write("%s\n" % trans)
    traceback.print_exc(None, sys.stderr)



def main(input_file_name):
    cust_file = os.path.join(PROJECT_ROOT, 'custs.csv')
    customers = {}
    product_file = os.path.join(PROJECT_ROOT, 'products.csv')
    products = {}

    head = "!TRNS	TRNSID	TRNSTYPE	DATE	ACCNT	NAME	CLASS	AMOUNT	DOCNUM	MEMO	CLEAR	TOPRINT	NAMEISTAXABLE	ADDR1	ADDR3	TERMS	SHIPVIA	SHIPDATE\r\n" \
        + "!SPL	SPLID	TRNSTYPE	DATE	ACCNT	NAME	CLASS	AMOUNT	DOCNUM	MEMO	CLEAR	QNTY	PRICE	INVITEM	TAXABLE	OTHER2	YEARTODATE	WAGEBASE\r\n" \
        + "!ENDTRNS\r\n"
    
    with open(cust_file, mode='r') as cst_file:
        reader = csv.reader(cst_file)
        for rows in reader:
            if reader.line_num == 1:
                continue
            if rows[0] != "":
                customers.update({rows[0]:rows[1]})

    with open(product_file, mode='r') as prd_file:
        reader = csv.reader(prd_file)
        for rows in reader:
            if reader.line_num == 1:
                continue
            if rows[0] != "":
                products.update({rows[0]:rows[1]})

    with open(input_file_name, mode='r') as our_file:
        reader = csv.reader(our_file)



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: python3 convertiif.py <yourinput.csv>")

    main(sys.argv[1])
