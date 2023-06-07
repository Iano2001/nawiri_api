import datetime
import uuid

from dateutil import parser
from flask import jsonify


def createShift(branch_id,
             sdate,
             shift_description,
             till_id):
    from app import mysql

    sql = """insert into shift (
    shift_id,
    branch_id,
    sdate,
    shift_complete,
    shift_day,
    shift_description,
    till_id,
    updated)
    values (
%s,%s,%s,%s,%s,%s,%s,%s
    )
;"""
    data = (uuid.uuid4(), branch_id, sdate, 'N', 'Y', shift_description, till_id, 'N',)
    cursor = mysql.connection.cursor()
    cursor.execute(sql, data)
    mysql.connection.commit()


def getRunningShift(branchId):
    from app import mysql
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT * FROM shift WHERE branch_id=%s AND shift_complete=%s ORDER BY sdate DESC LIMIT 1""",
                   (branchId, 'N',))
    result = cursor.fetchone()
    if result is None:
        return jsonify({"shift_id": "0"})
    cursor.close()
    return jsonify(result)


def getmyExpenses(branchId):
    from app import mysql
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT pay_id,
    branch_id,
    cash_amount,
    pay_date,
    pay_description,
    pay_ref,
    pay_to,
    pay_type_id,
    shift_id,
    till_id FROM pay_out WHERE pay_type_id=%s AND branch_id=%s""",
                   (5, branchId,))
    result = cursor.fetchall()
    if result is None:
        return jsonify([])
    cursor.close()
    return jsonify(result)


def ShiftsExpenses(
        branch_id,
        cash_amount,
        pay_date,
        pay_description,
        pay_ref,
        pay_to,
        shift_id,
        till_id):
    from app import mysql
    cursor = mysql.connection.cursor()
    query = """insert into pay_out (
    pay_id,
    branch_id,
    cash_amount,
    pay_amount,
    pay_date,
    pay_description,
    pay_ref,
    pay_time,
    pay_to,
    pay_type_id,
    shift_id,
    till_id)
values (
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
;"""
    today = parser.parse(pay_date)
    timePaid = datetime.datetime.strptime(str(today), "%Y-%m-%d %H:%M:%S")

    data = (
        uuid.uuid4(), branch_id, cash_amount, cash_amount, pay_date, pay_description, pay_ref, timePaid, pay_to, '5',
        shift_id, till_id,)
    cursor.execute(query, data)
    mysql.connection.commit()
