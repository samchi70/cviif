# Script to convert csv to IIF output.
import os
import sys, traceback, re
import csv

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

def error(trans):
    sys.stderr.write("%s\n" % trans)
    traceback.print_exc(None, sys.stderr)

def main():
    if len(sys.argv) <3:
        print("You need a transactions file and an invoice number")
        print("ex:python3 invoicescvt.py check#.csv 123")
        exit()

    input_file_name = sys.argv[1]
    invnum = int(sys.argv[2])
    cust_file = os.path.join(PROJECT_ROOT, 'custs.csv')
    product_file = os.path.join(PROJECT_ROOT, 'products.csv')
    invoice_dir = os.path.join(PROJECT_ROOT, 'invoices/')
    customers = dict()
    products = dict()
    transactions = list()
    current_trans = list()
    inv_trans = list()
    tmp_trans = list()
    customer = ""
    tmp_cust = ""
    prev_cust = ""
    product = ""
    tmp_product = ""
    trans_amount = 0
    inv_amount = 0
    check_date = ""

    head = "!TRNS\tTRNSID\tTRNSTYPE\tDATE\tACCNT\tNAME\tCLASS\tAMOUNT\tDOCNUM\tMEMO\tCLEAR\tTOPRINT\tNAMEISTAXABLE\tADDR1\tADDR3\tTERMS\tSHIPVIA\tSHIPDATE\r\n" \
    + "!SPL\tSPLID\tTRNSTYPE\tDATE\tACCNT\tNAME\tCLASS\tAMOUNT\tDOCNUM\tMEMO\tCLEAR\tQNTY\tPRICE\tINVITEM\tTAXABLE\tOTHER2\tYEARTODATE\tWAGEBASE\r\n" \
    + "!ENDTRNS\r\n"

    template1 = "TRNS\t\tINVOICE\t%s\tAccounts Receivable\t%s\t\t%s\t%s\t\tN\tN\tN\t\t\tDue on receipt\t\t%s\r\n"
    template2 = "SPL\t\tINVOICE\t%s\t%s\t\t\t-%s\t\t%s\tN\t\t%s\t\tN\t\t0\t0\r\n"
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
    
    inv_file = open(invoice_dir + 'inv' + str(invnum) + '.iif', mode = 'w')
    inv_file.write(head)

    for row in range(len(transactions)):
        if row == 0:
            tmp_trans = transactions[row]
            check_date = tmp_trans[1]
            tmp_trans.clear()
            continue
        
        if row > 0:            
            current_trans = transactions[row]
            tmp_cust = current_trans[0]

            if tmp_cust != "" and prev_cust =="":
                prev_cust = tmp_cust
                customer = customers.get(tmp_cust, "")
                tmp_product = current_trans[1]
                product = products.get(tmp_product, "")
                
                if customer == "":
                    error(tmp_cust)
                    exit(1)

                if product == "":
                    error(tmp_product)
                    exit(1)

                inv_amount += float(current_trans[2])
                trans_amount = float(current_trans[2])
                inv_trans.append([customer, product, tmp_product, trans_amount])
                continue
            
            if tmp_cust != "" and prev_cust == tmp_cust:
                tmp_product = current_trans[1]
                product = products.get(tmp_product, "")

                if product == "":
                    error(tmp_product)
                    exit(1)

                inv_amount += float(current_trans[2])
                trans_amount = float(current_trans[2])
                inv_trans.append([customer, product, tmp_product, trans_amount])
                continue

            if tmp_cust != "" and prev_cust != "" and tmp_cust != prev_cust:
                inv_file.write(template1 %(check_date, customer, inv_amount, invnum, check_date))
                for tmp_trans in inv_trans:
                    inv_file.write(template2 %(check_date,tmp_trans[1], tmp_trans[3],tmp_trans[2], tmp_trans[3])) 
                inv_file.write(trans_end)
                invnum += 1
                inv_trans.clear()
                inv_amount = 0

                prev_cust = tmp_cust
                customer = customers.get(tmp_cust, "")
                tmp_product = current_trans[1]
                product = products.get(tmp_product, "")
                
                if customer == "":
                    error(tmp_cust)
                    exit(1)

                if product == "":
                    error(tmp_product)
                    exit(1)

                inv_amount += float(current_trans[2])
                trans_amount = float(current_trans[2])
                inv_trans.append([customer, product, tmp_product, trans_amount])
                continue
       
    inv_file.close()

main()