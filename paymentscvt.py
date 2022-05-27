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
        print("You need a transactions file and begining invoice number")
        print("ex:python3 invoicescvt.py check#.csv 123")
        exit()

    input_file_name = sys.argv[1]
    invnum = int(sys.argv[2])
    cust_file = os.path.join(PROJECT_ROOT, 'custs.csv')
    invoice_dir = os.path.join(PROJECT_ROOT, 'invoices/')
    customers = dict()
    transactions = list()
    current_trans = list()
    tmp_trans = list()
    customer = ""
    tmp_cust = ""
    prev_cust = ""
    inv_amount = 0
    check_date = ""
    check_num = 0

    head = "!TRNS\tTRNSID\tTRNSTYPE\tDATE\tACCNT\tNAME\tAMOUNT\tDOCNUM\r\n" \
    + "!SPL\tSPLID\tTRNSTYPE\tDATE\tACCNT\tNAME\tAMOUNT\tDOCNUM\r\n" \
    + "!ENDTRNS\r\n"

    template1 = "TRNS\t\tPAYMENT\t%s\tUndeposited Funds\t%s\t%s\t%s\r\n"
    template2 = "SPL\t\tPAYMENT\t%s\tAccounts Receivable\t%s\t-%s\t%s\r\n"
    trans_end = "ENDTRNS\r\n"

    with open(cust_file, mode='r') as cst_file:
        reader = csv.reader(cst_file)
        for row in reader:
            if reader.line_num == 1:
                continue
            customers.update({row[0]:row[1]})
        cst_file.close()

    with open(os.path.join(PROJECT_ROOT, input_file_name), mode='r') as our_file:
        transactions = list(csv.reader(our_file))
        our_file.close()
   
    tmp_trans = transactions[0]
    check_num = int(tmp_trans[0])
    check_date = tmp_trans[1]
    tmp_trans.clear()

    pay_file = open(invoice_dir + 'pay' + str(check_num) + '.iif', mode = 'w')
    pay_file.write(head)

    for row in range(0, len(transactions)):
        print(row)
        if row == 0:
            continue
        
        if row == 1:
            continue

        if row > 1:            
            current_trans = transactions[row]
            tmp_cust = current_trans[0]

            if tmp_cust != "" and prev_cust =="":
                prev_cust = tmp_cust
                customer = customers.get(tmp_cust, "")
                
                if customer == "":
                    error(tmp_cust)
                    exit(1)

                inv_amount += float(current_trans[2])
            
            if tmp_cust != "" and prev_cust == tmp_cust:
                inv_amount += float(current_trans[2])

            if tmp_cust != "" and prev_cust != "" and tmp_cust != prev_cust:
                pay_file.write(template1 %(check_date, customer, inv_amount, invnum))
                pay_file.write(template2 %(check_date, customer, inv_amount, invnum))
                pay_file.write(trans_end)
                invnum += 1
                inv_amount = 0

                prev_cust = tmp_cust
                customer = customers.get(tmp_cust, "")
                
                if customer == "":
                    error(tmp_cust)
                    exit(1)

                inv_amount += float(current_trans[2])

    print(len(transactions))
    pay_file.close()

main()