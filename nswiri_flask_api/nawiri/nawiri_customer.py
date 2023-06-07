import uuid
from flask import jsonify


def nawiriaddCustomer(
        active,
        branch_id,
        bank_acc,
        status,
        credit_limit,
        name,
        phone_no,
        running_bal,
        total_credit,
        pin_number):
    sql = """insert into customer (
    customer_id,
    active,
    branch_id,
    customer_bank_acc,
    credit_status,
    customer_credit_limit,
    customer_name,
    customer_phone_no,
    customer_running_bal,
    customer_total_credit,
    pin_number,
    updated)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""

    from app import mysql
    cursor = mysql.connection.cursor()
    data = (
        uuid.uuid4(), active, branch_id,status, bank_acc, credit_limit, name, phone_no, running_bal, total_credit, pin_number,
        'Y',)
    cursor.execute(sql, data)
    mysql.connection.commit()
    cursor.close()


def getCustomerList(branchId):
    from app import mysql
    cursor = mysql.connection.cursor()
    sql = """SELECT customer_id,
    active,
    branch_id,
    customer_bank_acc,
    customer_credit_limit,
    customer_name,
    customer_phone_no,
    customer_running_bal,
    customer_total_credit,
    pin_number,
    updated FROM customer WHERE branch_id=%s"""
    data = (branchId,)
    cursor.execute(sql, data)
    result = cursor.fetchall()
    response = []

    for x in result:
        response.append(x)
    cursor.close()
    return response


def changeCustomerStatus(status, customerId):
    sql = """UPDATE customer SET active=%s WHERE customer_id=%s"""
    from app import mysql
    cursor = mysql.connection.cursor()
    cursor.execute(sql, (status, customerId,))
    mysql.connection.commit()
    cursor.close()


def nawiriUpdateCustomer(
        active,
        branch_id,
        account,
        limit,
        status,
        name,
        phone,
        balance,
        credit,
        pin):
    sql = """update customer set
    active=%s,
    customer_bank_acc=%s,
    customer_credit_limit=%s,
    customer_name=%s,
    credit_status=%s,
    customer_phone_no=%s,
    customer_total_credit=%s,
    pin_number=%s,
    updated=%s WHERE customer_id=%s"""

    from app import mysql
    cursor = mysql.connection.cursor()
    data = (active, account, limit,status,balance, name, phone, credit, pin,branch_id
            )
    cursor.execute(sql, data)
    mysql.connection.commit()
    cursor.close()
