import uuid

from flask import jsonify



def bankAdd(bank_name,account_details,updated_on,updated_by,
        account_manager,created_by,bank_acc_no,active,created_on,bank_running_bal,branch_id):
    from app import mysql
    cursor = mysql.connection.cursor()
    query = """insert into banks (
    bank_id,
    bank_name,
    account_details,
    updated_on,
    updated_by
    account_manager,
    created_by,
    bank_acc_no,
    active,
    created_on,
    bank_running_bal,
    branch_id
   )
values (%s,%s,%s,%s,%s,%s,%s,%s)
;"""
    data = (uuid.uuid4(),bank_name,account_details,updated_on,updated_by, account_manager, created_by, bank_acc_no, active, created_on, bank_running_bal, branch_id)
    cursor.execute(query, data)
    mysql.connection.commit()
    cursor.close()


def getBranchBanks(branchId):
    from app import mysql
    cursor = mysql.connection.cursor()
    query = """SELECT * FROM banks WHERE branch_id=%s"""
    cursor.execute(query, (branchId,))
    results = cursor.fetchall()
    if results is None or len(results) < 1:
        return jsonify([])
    return jsonify(results)

def updateRunningBalance(newVal, bankId):
        from app import mysql
        cursor = mysql.connection.cursor()
        query = """UPDATE banks SET bank_running_bal=%s WHERE bank_id=%s"""
        cursor.execute(query, (newVal, bankId,))
        mysql.connection.commit()
        cursor.close()

def getCurrentRunningBal(bankId):
        from app import mysql
        cursor = mysql.connection.cursor()
        query = """SELECT bank_running_bal FROM banks WHERE bank_id=%s"""
        cursor.execute(query, (bankId,))
        result = cursor.fetchone()
        if result is None:
            return 0
        return int(result["bank_running_bal"])
def addTransaction(
            bank_id,
            bank_trans_type_id,
            branch_id,
            created_by,
            created_on,
            trans_amount,
            trans_comment,
            trans_date,
            trans_ref,
            trans_complete, sign):
        from app import mysql
        cursor = mysql.connection.cursor()

        currentbal = getCurrentRunningBal(bank_id)
        if sign == "-":
            currentbal = currentbal - int(trans_amount)
        else:
            currentbal = currentbal + int(trans_amount)

        query = """insert into bank_trans (
        bank_trans_id,
        bank_id,
        bank_trans_type_id,
        branch_id,
        created_by,
        created_on,
        trans_amount,
        trans_comment,
        trans_date,
        trans_ref,
        trans_running_bal,
        trans_complete
       )
    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    ;"""
        data = (
        uuid.uuid4(), bank_id, bank_trans_type_id, branch_id, created_by, created_on, trans_amount, trans_comment,
        trans_date, trans_ref, currentbal, trans_complete,)
        cursor.execute(query, data)
        mysql.connection.commit()
        cursor.close()
        updateRunningBalance(currentbal, bank_id)

def newgetBankTransactions(branchId):
        query = """SELECT * FROM bank_trans WHERE branch_id=%s"""
        from app import mysql
        cursor = mysql.connection.cursor()
        cursor.execute(query, (branchId,))
        results = cursor.fetchall()
        if results is None or len(results) < 1:
            return jsonify([])
        return jsonify(results)




