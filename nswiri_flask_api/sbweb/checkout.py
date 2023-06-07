import datetime
import uuid

from sbweb.company import getParameterInfo
from flask import jsonify


def createPosReceipt(
        branch_id,
        customer_id,
        location_id,
        receipt_cash_amount,
        receipt_bank_amount,
        receipt_mobile_money,
        receipt_total_amount,
        shift_id,
        staff_id,
        till_id,
        cart):
    from app import mysql
    cursor = mysql.connection.cursor()
    query = """insert into pos_receipts (
                receipt_id,
                bill_printed,
                branch_id,
                cancelled,
                comments,
                customer_id,
                location_id,
                receipt_card_amount,
                receipt_cash_amount,
                receipt_cheque_amount,
                receipt_code,
                receipt_date,
                receipt_discount,
                receipt_mobile_money,
                receipt_paid,
                receipt_ref,
                receipt_time,
                receipt_total_amount,
                receipt_voucher_amount,
                service_customer_id,
                shift_id,
                staff_id,
                till_id,
                updated)
            values (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
               )
            ;"""
    paramInfo = getParameterInfo(branch_id)
    if "value" in paramInfo:
        code = str(paramInfo.get("value") + 1).zfill(6)
    else:
        code = str(paramInfo.get("invoice_no")).zfill(6)
    rId = uuid.uuid4()
    data = (rId, 'N', branch_id, 'N', "POS Sale", customer_id, location_id,
            receipt_bank_amount, receipt_cash_amount, '0', code, datetime.date.today(), '0', receipt_mobile_money,
            'Y', code, datetime.datetime.now().strftime("%H:%M:%S"), receipt_total_amount, '0', customer_id, shift_id,
            staff_id, till_id,
            'N',)
    cursor.execute(query, data)


    #update parameter file
    sql = """UPDATE parameter_file SET invoice_no=%s WHERE branch_id=%s"""
    cursor.execute(sql, (int(code) + 1, branch_id,))
    mysql.connection.commit()
    cursor.close()
    addPosReceiptDetails(branch_id, cart, rId, location_id, code, staff_id, shift_id, till_id, receipt_total_amount)


def addPosReceiptDetails(
        branch_id,
        cartItem,
        receipt_id,
        location, 
        code,
        staff_id,
        shift_id,
        till_id,
        receipt_total_amount,
        ):
    query = """insert into pos_receipt_details (
            receipt_details_id,
            branch_id,
            cancelled,
            discount,
            linenum,
            location_product_id,
            product_bp,
            product_sp,
            receipt_id,
            trans_quantity,
            uom_code,
            updated)
        values (
           %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ;"""

    from app import mysql
    cursor = mysql.connection.cursor()
    count = 1

    #insert into payment details
    pos_payment_query = """insert into pos_receipt_payment (
                            pos_receipt_payment_id,
                            receipt_id,
                            payment_date,
                            staff_id,
                            shift_id,
                            till_id,
                            cancelled,
                            payment_amount)
                        values (
                           %s,%s,%s,%s,%s,%s,%s,%s)
                        ;"""

    payment_details_data = (uuid.uuid4(), receipt_id, datetime.datetime.now(),staff_id, shift_id, till_id, "N", receipt_total_amount,)

    cursor.execute(pos_payment_query, payment_details_data)



    #insert into pos_details
    for item in cartItem:
        product = item["product"]
        print (product)
        
        data = (uuid.uuid4(), branch_id, 'N', '0', count, product["location_product_id"],
                product["product_bp"], product["location_product_sp"], receipt_id, float(item["quantity"]), product["uom_code"], 'N',)
        cursor.execute(query, data)

        q = """UPDATE location_stock SET location_product_quantity=%s WHERE 
        location_product_id=%s"""
        cursor.execute(q, (int(float(product["location_product_quantity"])) - int(float(item["quantity"])),
                           product["location_product_id"],))
        q = """insert into trans_file (
            trans_id,
            branch_id,
            cancelled,
            complete,
            confirmed,
            cost_price,
            created_on,
            location_id,
            location_product_id,
            running_balance,
            sprice,
            trans_comment,
            trans_date,
            trans_quantity,
            trans_reference,
            trans_type_id,
            uom_code,
            updated
            )
        values (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ;"""

        data = (uuid.uuid4(), branch_id, 'N', 'Y', 'Y', (int(product["product_bp"]) * int(item["quantity"])),
                datetime.datetime.now(), location, product["location_product_quantity"],
                int(float(product["location_product_quantity"])) - int(float(item["quantity"])), product["product_bp"],
                "POS Sale", datetime.datetime.now(), item["quantity"], code, '1', product["uom_code"], 'N',)
        cursor.execute(q, data)

    mysql.connection.commit()


def fetchCreatedReceipts(branch_id):
    query = "SELECT * FROM pos_receipts WHERE branch_id = %s"
    from app import mysql
    cursor = mysql.connection.cursor()
    cursor.execute(query, (branch_id,))
    
    receipts = cursor.fetchall()  
    print (receipts)
    if receipts is None or len(receipts) < 1:
        return jsonify([])
    return jsonify(list(receipts))

    


