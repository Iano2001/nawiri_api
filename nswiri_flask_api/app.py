import datetime
import hashlib
import json
import time
import uuid
from uuid import UUID

import bcrypt
from dateutil.relativedelta import relativedelta
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL

from sbweb.banks import addBank, updateBank, deleteBank, getBankList, addTransaction, getBankTransactions
from sbweb.checkout import *
from sbweb.company import createCompany, setPaid, getBranchDetails, getCurrentCompany, createBranch, getAllMyBranches, \
    subscriptionStatus
from sbweb.customers import addCustomer, getCustomerList, changeCustomerStatus, updateCustomer
from sbweb.helpers import getLocations
from sbweb.inventory import addUom, getUoms, deleteUom, editUom, addCategory, getCategories, deleteCategory, editCategory, \
    getNextScanCode, addInventory, getInventoryList, deactivateProduct, activateProduct, receiveStock
from sbweb.shifts import addShift, getRunningShift, addExpense, getExpenses
from sbweb.suppliers import addSupplier, getSupplierList, changeSupplierStatus, updateSupplier, getCurrentRunningBalance, \
    addPayment, getTransactionList, getTransactionListFilteredFrom, getTransactionListFilteredTo, \
    getTransactionListFiltered
from sbweb.transactions import getTransactionTypes
from nawiri.nawiri_inventory import *
from nawiri.nawiri_bank import *
from nawiri.nawiri_customer import *
from nawiri.nawiri_company import *
from nawiri.nawiri_shift import *
from nawiri.nawiri_suppliers import *

app = Flask(__name__)
CORS(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'iano2001'
app.config['MYSQL_DB'] = 'sbpos'
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

#START OF SBWEB APIS
@app.route("/", methods=["GET", "POST"])
def home():
    return "You are here"


@app.route("/createUser", methods=["POST"])
@cross_origin()
def createUser():
    companyEmail = request.form.to_dict().get("company[email]")
    username = request.form.to_dict().get("user[name]")
    userphone = request.form.to_dict().get("user[phone]")
    userref = request.form.to_dict().get("user[ref]")
    userpassword = request.form.to_dict().get("user[password]")
    companyname = request.form.to_dict().get("company[name]")
    companylocation = request.form.to_dict().get("company[location]")
    companytill = request.form.to_dict().get("company[till]")
    companyreceipt = request.form.to_dict().get("company[receipt]")

    userpassword = hashlib.sha256(userpassword.encode("utf-8")).hexdigest()

    sql2 = """SELECT user_id FROM sys_user WHERE user_pin=%s"""
    data = (companyEmail,)

    cursor = mysql.connection.cursor()
    cursor.execute(sql2, data)
    rows = cursor.fetchone()
    mysql.connection.commit()
    if rows is not None:
        cursor.close()
        return jsonify({"success": False, "message": "Email is already registered"})

    # print("Staff Code:", staff_code)

    #Create User
    sql = """INSERT INTO sys_user(user_id,staff_id,User_name,user_pass,user_pin,updated,branch_id,referal_code,paid)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    branchId = int(time.time_ns() & 0xffff)
    data = (uuid.uuid4(), 0, username, userpassword, companyEmail, "N", branchId, userref, "N",)
    cursor.execute(sql, data)
    mysql.connection.commit()

    sql = """insert into parameter_file (
    parameter_id,
    branch_id,
    categoryno,
    customerno,
    expence_no,
    foliono,
    fscan,
    grn_no,
    invoice_no,
    jobno,
    lpo_no,
    quote_no,
    rmargin,
    staffno,
    supplierno,
    updated,
    wmargin)
values (
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
;"""
    data = (uuid.uuid4(), branchId, '0', '0', '0', '0', 'N', '0', '0', '0', '0', '0', '0', '0', '0', 'N', '0',)
    cursor.execute(sql, data)
    mysql.connection.commit()

    ##Create Company
    companyId = createCompany(companyname, userphone, companylocation, companyEmail, companytill, branchId)
    cursor.close()

    return jsonify({"success": True, "message": "Created User", "branchId": branchId, "companyId": companyId})


@app.route("/loginUser", methods=["POST"])
@cross_origin()
def loginUser():
    username = request.form.to_dict().get("email")
    password = request.form.to_dict().get("password")
    userpassword = hashlib.sha256(password.encode("utf-8")).hexdigest()

    cursor = mysql.connection.cursor()
    sql = """SELECT user_id,staff_id,user_name,updated,branch_id,referal_code,paid FROM sys_user WHERE user_pin=%s 
    AND user_pass=%s"""
    cursor.execute(sql, (username, userpassword,))
    users = cursor.fetchone()
    if users == None:
        return jsonify({"success": False, "message": "Invalid email or password"})
    response = {"success": True, "message": "User Logged In", "user": users}

    sql = """SELECT company_id, company_name,company_tel,company_town,company_address,payment_details FROM company WHERE 
    company_address=%s"""
    cursor.execute(sql, (username,))
    company = cursor.fetchone()
    response["company"] = company
    cursor.close()
    return jsonify(response)


@app.route("/setPaid", methods=["POST"])
def markPaid():
    amount = request.form.to_dict().get("amount")
    plan = request.form.to_dict().get("plan")
    email = request.form.to_dict().get("email")
    branchId = request.form.to_dict().get("branchId")
    setPaid(plan, email, branchId, amount)

    return jsonify({"success": True, "message": "Activated"})


@app.route("/addUom", methods=["POST"])
def addUnitOfMeasurement():
    branchId = request.form.to_dict().get("branchId")
    code = request.form.to_dict().get("code")
    desc = request.form.to_dict().get("desc")
    addUom(branchId, code, desc)
    return jsonify({"success": True, "message": "UOM added"})


@app.route("/getBranchUoms", methods=["POST"])
def getUomsList():
    branchId = request.form.to_dict().get("branch")
    resp = getUoms(branchId)
    return jsonify(resp)


@app.route("/deleteUom", methods=["POST"])
def deleteSingleUom():
    uomId = request.form.to_dict().get("id")
    deleteUom(uomId)
    return jsonify({"success": True, "message": "UOM deleted"})


@app.route("/editUom", methods=["POST"])
def editSingleUom():
    uomId = request.form.to_dict().get("id")
    code = request.form.to_dict().get("code")
    desc = request.form.to_dict().get("desc")
    editUom(uomId, code, desc)
    return jsonify({"success": True, "message": "UOM edited"})


@app.route("/addCategory", methods=["POST"])
def addProductCategory():
    branchId = request.form.to_dict().get("branchId")
    name = request.form.to_dict().get("name")
    wm = request.form.to_dict().get("wm")
    rm = request.form.to_dict().get("rm")
    addCategory(branchId, wm, rm, name)
    return jsonify({"success": True, "message": "UOM edited"})


@app.route("/getBranchCategories", methods=["POST"])
def getBranchCategories():
    branchId = request.form.to_dict().get("branch")
    return jsonify(getCategories(branchId))


@app.route("/deleteCategory", methods=["POST"])
def deleteSingleCategory():
    categoryId = request.form.to_dict().get("id")
    deleteCategory(categoryId)
    return jsonify({"success": True, "message": "UOM deleted"})


@app.route("/editCategory", methods=["POST"])
def editSingleCategory():
    categoryId = request.form.to_dict().get("id")
    name = request.form.to_dict().get("name")
    wm = request.form.to_dict().get("wm")
    rm = request.form.to_dict().get("rm")
    editCategory(categoryId, name, wm, rm)
    return jsonify({"success": True, "message": "UOM edited"})


@app.route("/nextScanCode", methods=["POST"])
def getNextProductScanCode():
    branchId = request.form.to_dict().get("branch")
    return jsonify(getNextScanCode(branchId))


@app.route("/addInventory", methods=["POST"])
def newInventory():
    uomCode = request.form.to_dict().get("uomcode")
    name = request.form.to_dict().get("name")
    categoryId = request.form.to_dict().get("category")
    scancode = request.form.to_dict().get("code")
    bp = request.form.to_dict().get("bp")
    wp = request.form.to_dict().get("wp")
    rp = request.form.to_dict().get("rp")
    bn = request.form.to_dict().get("bn")
    active = request.form.to_dict().get("active")
    branchId = request.form.to_dict().get("branch")
    qtty = request.form.to_dict().get("quantity")

    addInventory(active, bn, branchId, categoryId, name, qtty, scancode, rp, wp, uomCode, bp)
    return jsonify({"success": True, "message": "Inventory Added"})


@app.route("/getInventory", methods=["POST"])
def getInventory():
    branchId = request.form.to_dict().get("branch")
    return jsonify(getInventoryList(branchId))


@app.route("/deactivateProduct", methods=["POST"])
def deactivateItem():
    itemId = request.form.to_dict().get("id")
    deactivateProduct(itemId)
    return jsonify({"success": True, "message": "Inventory Deactivated"})


@app.route("/activateProduct", methods=["POST"])
def activateItem():
    itemId = request.form.to_dict().get("id")
    activateProduct(itemId)
    return jsonify({"success": True, "message": "Inventory Activated"})


@app.route("/productLocations", methods=["POST"])
def getProductLocations():
    return getLocations()


@app.route("/newCustomer", methods=["POST"])
def newCustomer():
    account = request.form.to_dict().get("account")
    name = request.form.to_dict().get("name")
    status = request.form.to_dict().get("status")
    phone = request.form.to_dict().get("phone")
    balance = request.form.to_dict().get("balance")
    credit = request.form.to_dict().get("credit")
    limit = request.form.to_dict().get("limit")
    pin = request.form.to_dict().get("pin")
    branchId = request.form.to_dict().get("branch")
    newaddCustomer(status, branchId, account, limit, name, phone, balance, credit, pin)
    return jsonify({"success": True, "message": "Customer Added"})


@app.route("/getCustomerList", methods=["POST"])
def getMyCustomers():
    branchId = request.form.to_dict().get("branch")
    return jsonify(getCustomerList(branchId))


@app.route("/changeCustomerStatus", methods=["POST"])
def changeMyCustomerStatus():
    status = request.form.to_dict().get("status")
    customerId = request.form.to_dict().get("id")
    changeCustomerStatus(status, customerId)
    return jsonify({"success": True, "message": "Customer Updated"})


@app.route("/updateCustomer", methods=["POST"])
def updateMyCustomer():
    account = request.form.to_dict().get("account")
    name = request.form.to_dict().get("name")
    status = request.form.to_dict().get("status")
    phone = request.form.to_dict().get("phone")
    credit = request.form.to_dict().get("credit")
    limit = request.form.to_dict().get("limit")
    pin = request.form.to_dict().get("pin")
    customerId = request.form.to_dict().get("customerId")
    updateCustomer(status, account, limit, name, phone, credit, pin, customerId)
    return jsonify({"success": True, "message": "Customer Updated"})


@app.route("/newSupplier", methods=["POST"])
def newSupplier():
    account = request.form.to_dict().get("account")
    name = request.form.to_dict().get("name")
    phone = request.form.to_dict().get("phone")
    address = request.form.to_dict().get("address")
    pin = request.form.to_dict().get("pin")
    branchId = request.form.to_dict().get("branch")
    balance = request.form.to_dict().get("balance")

    addSupplier(branchId, account, address, name, phone, balance, pin)
    return jsonify({"success": True, "message": "Customer Added"})


@app.route("/getSupplierList", methods=["POST"])
def getMySuppliers():
    branchId = request.form.to_dict().get("branch")
    return jsonify(getSupplierList(branchId))


@app.route("/changeSupplierStatus", methods=["POST"])
def changeMySupplierStatus():
    status = request.form.to_dict().get("status")
    customerId = request.form.to_dict().get("id")
    changeSupplierStatus(status, customerId)
    return jsonify({"success": True, "message": "Supplier Updated"})


@app.route("/updateSupplier", methods=["POST"])
def updateMySupplier():
    account = request.form.to_dict().get("account")
    name = request.form.to_dict().get("name")
    phone = request.form.to_dict().get("phone")
    address = request.form.to_dict().get("address")
    pin = request.form.to_dict().get("pin")
    balance = request.form.to_dict().get("balance")
    supplierId = request.form.to_dict().get("supplierId")
    print("Supplier ID:", supplierId, "balance:", balance)
    updateSupplier(supplierId, account, address, name, phone, pin, balance)
    return jsonify({"success": True, "message": "Supplier Updated"})


@app.route("/getTransactionTypes", methods=["POST"])
def getTransTypes():
    return getTransactionTypes()


@app.route("/addSupplierPayment", methods=["POST"])
def addPayments():
    branchId = request.form.to_dict().get("branch")
    createdBy = request.form.to_dict().get("createdBy")
    createdOn = request.form.to_dict().get("createdOn")
    transTypeId = request.form.to_dict().get("type")
    amount = request.form.to_dict().get("amount")
    comment = request.form.to_dict().get("comments")
    ref = request.form.to_dict().get("reference")
    supplierId = request.form.to_dict().get("supplierId")
    addPayment(supplierId, branchId, createdBy, createdOn, transTypeId, amount, comment, ref)
    return jsonify({"success": True, "message": "Payment Added"})


@app.route("/getSupplierTrans", methods=["POST"])
def getSupTrans():
    supplierId = request.form.to_dict().get("supplierId")
    return getTransactionList(supplierId)


@app.route("/getSupplierTransFiltered", methods=["POST"])
def getSupplierTransFiltered():
    supplierId = request.form.to_dict().get("supplierId")
    fromDate = request.form.to_dict().get("from")
    to = request.form.to_dict().get("to")
    if fromDate == "":
        return getTransactionListFilteredTo(supplierId, to)
    elif to == "":
        return getTransactionListFilteredFrom(supplierId, fromDate)
    else:
        return getTransactionListFiltered(supplierId, fromDate, to)


@app.route("/newBank", methods=["POST"])
def newBank():
    account_details = request.form.to_dict().get("branchName")
    bank_acc_no = request.form.to_dict().get("account")
    bank_name = request.form.to_dict().get("name")
    branch_id = request.form.to_dict().get("branch")
    phone = request.form.to_dict().get("phone")
    addBank(account_details, bank_acc_no, bank_name, branch_id, phone)
    return jsonify({"success": True, "message": "Bank Added"})


@app.route("/updateBank", methods=["POST"])
def updateABank():
    account_details = request.form.to_dict().get("branchName")
    bank_acc_no = request.form.to_dict().get("account")
    bank_name = request.form.to_dict().get("name")
    phone = request.form.to_dict().get("phone")
    bankId = request.form.to_dict().get("id")
    updateBank(account_details, bank_acc_no, bank_name, phone, bankId)
    return jsonify({"success": True, "message": "Bank Updated"})


@app.route("/deleteBank", methods=["POST"])
def removeBank():
    bankId = request.form.to_dict().get("id")
    deleteBank(bankId)
    return jsonify({"success": True, "message": "Bank Deleted"})


@app.route("/listBanks", methods=["POST"])
def listBanks():
    branch_id = request.form.to_dict().get("branch")
    return getBankList(branch_id)


@app.route("/bankTransaction", methods=["POST"])
def addBankTransaction():
    bank_id = request.form.to_dict().get("bankId")
    bank_trans_type_id = request.form.to_dict().get("type")
    branch_id = request.form.to_dict().get("branch")
    created_by = request.form.to_dict().get("createdBy")
    created_on = request.form.to_dict().get("createdOn")
    trans_amount = request.form.to_dict().get("amount")
    trans_comment = request.form.to_dict().get("comments")
    trans_date = created_on
    trans_ref = request.form.to_dict().get("ref"),
    trans_complete = request.form.to_dict().get("complete")
    sign = request.form.to_dict().get("sign")
    addTransaction(bank_id, bank_trans_type_id, branch_id, created_by, created_on, trans_amount, trans_comment,
                   trans_date, trans_ref, trans_complete, sign)
    return jsonify({"success": True, "message": "Transaction Added"})


@app.route("/bankTransactionsList", methods=["POST"])
def newbankTransactionsList():
    branch_id = request.form.to_dict().get("branch")
    return newgetBankTransactions(branch_id)


@app.route("/newShift", methods=["POST"])
def newShift():
    branchId = request.form.to_dict().get("branch")
    sdate = request.form.to_dict().get("date"),
    shift_description = request.form.to_dict().get("desc"),
    till_id = request.form.to_dict().get("till")
    addShift(branchId, sdate, shift_description, till_id)
    return jsonify({"success": True, "message": "Shift Started"})


@app.route("/runningShift", methods=["POST"])
def runningShift():
    branchId = request.form.to_dict().get("branch")
    return getRunningShift(branchId)


@app.route("/newExpense", methods=["POST"])
def newExpense():
    branch_id = request.form.to_dict().get("branch")
    cash_amount = request.form.to_dict().get("amount")
    pay_date = request.form.to_dict().get("date")
    pay_description = request.form.to_dict().get("desc")
    pay_ref = request.form.to_dict().get("ref")
    pay_to = request.form.to_dict().get("to")
    shift_id = request.form.to_dict().get("shift")
    till_id = request.form.to_dict().get("till")
    addExpense(branch_id, cash_amount, pay_date, pay_description, pay_ref, pay_to, shift_id, till_id)
    return jsonify({"success": True, "message": "Expense Added"})


@app.route("/getExpenses", methods=["POST"])
def getMyExpenses():
    branch_id = request.form.to_dict().get("branch")
    print(branch_id)
    return getExpenses(branch_id)


@app.route("/posCheckout", methods=["POST"])
def getCartCheckout():
    data = request.get_json()  # Retrieve JSON data from the request

    branch_id = data.get("branch")
    total = data.get("total")
    cash = data.get("cash")
    mpesa = data.get("mpesa")
    bank = data.get("bank")
    shift_id = data.get("shift")
    till_id = data.get("till")
    customerId = data.get("customerId")
    staffId = data.get("staffId")
    location = data.get("location")
    cart = data.get("cart")

    print(branch_id)
    

    createPosReceipt(branch_id, customerId, location, cash, bank, mpesa, total, shift_id, staffId, till_id, cart)
    return jsonify({"success": True, "message": "Checkout success"})


@app.route("/receiveStock", methods=["POST"])
def receiveSuppStock():
    qtty = request.form.to_dict().get("quantity")
    sp = request.form.to_dict().get("sellingPrice")
    bp = request.form.to_dict().get("buyingPrice")
    pid = request.form.to_dict().get("product")
    newBal = request.form.to_dict().get("amount")
    supplierId = request.form.to_dict().get("supplierId")
    return receiveStock(qtty, sp, bp, pid, newBal, supplierId)


@app.route("/branchDetails", methods=["POST"])
def branchDetails():
    branch_id = request.form.to_dict().get("branch")
    return getBranchDetails(branch_id)


@app.route("/companyDetails", methods=["POST"])
def companyDetails():
    email = request.form.to_dict().get("email")
    return getCurrentCompany(email)


@app.route("/addBranch", methods=["POST"])
def newCompanyBranch():
    branchId = int(time.time_ns() & 0xffff)
    company = request.form.to_dict().get("company")
    amount = request.form.to_dict().get("amount")
    name = request.form.to_dict().get("name")
    phone = request.form.to_dict().get("phone")
    createBranch(company, branchId, name, phone)
    today = datetime.datetime.now()
    endDate = today + relativedelta(months=+1)
    cursor = mysql.connection.cursor()
    sql = """INSERT INTO subscription (branch_id,plan,amount,payment_method,start_date,end_date,status)VALUES(%s,%s,%s,%s,
        %s,%s,%s)"""
    data = (branchId, "monthly", amount, "Mpesa", today, endDate, "Active",)
    cursor.execute(sql, data)
    mysql.connection.commit()
    return jsonify({"success": True})


@app.route("/companyBranches", methods=["POST"])
def getCompanyBranches():
    company = request.form.to_dict().get("company")
    return getAllMyBranches(company)


@app.route("/branchSubscription", methods=["POST"])
def getBranchSubscription():
    branch = request.form.to_dict().get("branch")
    return subscriptionStatus(branch)

@app.route("/getBranchSales", methods=["POST"])
def getBranchsales():
    branch_id = request.form.to_dict().get("branch")
    return fetchCreatedReceipts(branch_id)
# END OF SBWEB API 



# START OF NAWIRI API
@app.route("/newuom", methods=["POST"])
def nawiriUom():
        data = request.get_json()
        branchId = data.get("branch_id")
        code = data.get("uom_code")
        desc = data.get("uom_description")
        updated=""
        print(code)
        createUom(branchId, code, desc)
        return jsonify({"success": True, "message": "UOM create"})

@app.route("/newupdateUom", methods=["PATCH"])
def newupdateUom():
        UomId = request.form.to_dict().get("Uom_id")
        code = request.form.to_dict().get("uom_code")
        desc = request.form.to_dict().get("uom_description")
        updated = ""
        updateUom(UomId, code, desc)
        return jsonify({"success": True, "message": "UOM updated"})

@app.route("/newgetUom", methods=["POST"])
def newBranchUomget():
        data = request.get_json()
        branch_id = data.get("branch_id")
        print(branch_id)
        return getBranchUoms(branch_id)



@app.route("/newcategories", methods=["POST"])
def newaddCategory():
    data = request.get_json()
    # Retrieve the values from the dictionary
    branchId = data.get("branch_id")
    name = data.get("category_desc")
    show_in_pos=data.get("Show_in_pos")
    wm = data.get("wmargin")
    rm = data.get("rmargin")

    print (wm)
    
    createCategory(branchId, wm, rm, name, show_in_pos)
    return jsonify({"success": True, "message": "category  added"})

@app.route("/getnewcategories", methods=["POST"])
def newgetCategories():
        data = request.get_json()
        branch_id = data.get("branch_id")
        print(branch_id)
        return getBranchCategories(branch_id)

@app.route("/newupdateCategory", methods=["PATCH"])
def updateProductCategory():
        categoryId = request.form.to_dict().get("categoryId")
        name = request.form.to_dict().get("name")
        wm = request.form.to_dict().get("wm")
        rm = request.form.to_dict().get("rm")
        updateCategory(categoryId, wm, rm, name)
        return jsonify({"success": True, "message": "category updated"})

@app.route("/newnextScanCode", methods=["POST"])
def getNextScanCode():
        data = request.get_json()
        branch_id = data.get("branch_id")
        return getNextScanCode(branch_id)

@app.route("/createproduct", methods=["POST"])
def newproduct():
        data = request.get_json()
        uomCode = data.get("uom_code")
        name = data.get("product_name")
        categoryId = data.get("category_id")
        scancode = data.get("location_product_scancode")
        bp = data.get("product_bp")
        wp = data.get("location_product_sp1")
        rp = data.get("location_product_sp")
        bn = data.get("fixed_price")
        active = data.get("active")
        branchId = data.get("branch_id")
        qtty = data.get("location_product_quantity")

        createProduct(active, bn, branchId, categoryId,name, qtty, scancode, rp, wp, uomCode, bp)
        return jsonify({"success": True, "message": "product Added"})

@app.route("/newgetProducts", methods=["POST"])
def getProducts():
        data = request.get_json()
        branch_id = data.get("branch")
        print(branch_id)
        return getProducts(branch_id)

@app.route("/receivesupStock", methods=["PATCH"])
def receivesupStock():
        qtty = request.form.to_dict().get("trans_quantity")
        sp = request.form.to_dict().get("sprice")
        bp = request.form.to_dict().get("cost_price")
        pid = request.form.to_dict().get("location_product_id")
        newBal = request.form.to_dict().get("trans_type")
        supplierId = request.form.to_dict().get("supplier_id")
        receiveBranchStock(qtty, sp, bp, pid, newBal, supplierId)
        return jsonify({"success": True, "message": "Stock received"})




@app.route("/addbank", methods=["POST"])
def createNawiriBank():
    data = request.get_json()

    bank_name = data.get("bank_name")
    account_manager = data.get("account_manager")
    account_details = data.get("account_details")
    created_by=data.get("created_by")
    active="Y"
    created_on=datetime.datetime.now()
    updated_by=None
    updated_on=None
    bank_running_bal="0"
    bank_acc_no=data.get("bank_acc_no")
    branch_id = data.get("branch_id")
    
    bankAdd(bank_name,account_details,updated_on,updated_by,
        account_manager,created_by,bank_acc_no,active,created_on,bank_running_bal,branch_id)
    return jsonify({"success": True, "message": "Bank Added"})

@app.route("/newgetbanks", methods=["POST"])
def getBranchBankList():
    data = request.get_json()
    branchId=data.get("branch_id")
    return getBranchBanks(branchId)

@app.route("/newbankTransaction", methods=["POST"])
def newaddBankTransaction():
        data = request.get_json()
        bank_id = data.get("bank_id")
        bank_trans_type_id = data.get("transtype")
        branch_id = data.get("branch_id")
        created_by = data.get("created_by")
        created_on = data.get("created_on")
        trans_amount = data.get("transaction_amount")
        trans_comment = data.get("transaction_comment")
        trans_date = created_on
        trans_ref = data.get("transaction_ref"),
        trans_complete = data.get("trans_complete")
        sign = data.get("sign")
        addTransaction(bank_id, bank_trans_type_id, branch_id, created_by, created_on, trans_amount, trans_comment,
                       trans_date, trans_ref, trans_complete, sign)
        return jsonify({"success": True, "message": "Transaction Added"})

@app.route("/getTransactions", methods=["POST"])
def getBankTransactions():
        data = request.get_json()
        branchId = data.get("branch_id")
        print(branchId)
        return newgetBankTransactions(branchId)


@app.route("/newaddCustomer", methods=["POST"])
def addCustomer():
        data = request.get_json()
        bank_acc = data.get("customer_acc")
        name = data.get("customer_name")
        status = data.get("credit_status")
        active=""
        phone_no = data.get("customer_phone_no")
        running_bal = data.get("customer_running_bal")
        total_credit = data.get("credit_period")
        credit_limit = data.get("customer_credit_limit")
        pin_number = data.get("pin_number")
        branch_id = data.get("branch_id")
        nawiriaddCustomer(active,branch_id,status, bank_acc,credit_limit, name,phone_no,running_bal,total_credit,pin_number)
        return jsonify({"success": True, "message": "Customer Added"})

@app.route("/getCustomers", methods=["POST"])
def getCustomerList():
        data = request.get_json()
        branch_id = data.get("branch")
        print(branch_id)
        return getCustomerList(branch_id)

@app.route("/changeCustomerStatus", methods=["POST"])
def newchangeCustomerStatus():
        data = request.get_json()
        status = data.get("status")
        customerId = data.get("id")
        changeCustomerStatus(status, customerId)
        return jsonify({"success": True, "message": "Customer status Updated"})

@app.route("/newupdateCustomer", methods=["PATCH"])
def newupdateCustomer():
        account = request.form.to_dict().get("customer_acc")
        name = request.form.to_dict().get("customer_name")
        status = request.form.to_dict().get("credit_status")
        active = ""
        phone = request.form.to_dict().get("customer_phone_no")
        balance = request.form.to_dict().get("customer_running_bal")
        credit = request.form.to_dict().get("credit_period")
        limit = request.form.to_dict().get("customer_credit_limit")
        pin = request.form.to_dict().get("pin_number")
        branchId = request.form.to_dict().get("branch_id")
        nawiriUpdateCustomer(active, branchId,status, account, limit, name, phone, balance, credit, pin)
        return jsonify({"success": True, "message": "Customer updated"})

@app.route("/createnewCompany", methods=["POST"])
def createCompanynew():
        data = request.get_json()
        cName = data.get("company_name")
        cTel = data.get("company_tel")
        cTown = data.get("company_town")
        cAddress = data.get("company_address")
        cPayment = data.get("payment_details")
        branchId = data.get("branchId")
        newcreateCompany(cName,cTel,cTown,cAddress,cPayment,branchId)
        return jsonify({"success": True, "message": "company created"})



@app.route("/createBranch", methods=["POST"])
def newcreateBranch():
        data = request.get_json()
        companyId = data.get("company_id")
        companyName = data.get("branch_name")
        contact = data.get("branchcontact")
        branchId = data.get("branch_id")

        createBranch(companyId, branchId, companyName, contact)
        return jsonify({"success": True, "message": "company created"})

@app.route("/getbranchDetails", methods=["POST"])
def newbranchDetails():
        data = request.get_json()
        branchId = data.get("branch")
        return getBranchDetails(branchId)

@app.route("/getParameterInfo", methods=["POST"])
def getParameterInfo():
        data = request.get_json()
        branchId = data.get("branch")
        return getParameterInfo(branchId)

@app.route("/updateInvoiceNo", methods=["PATCH"])
def updateInvoiceNo():
    branchId = request.form.to_dict().get("branch_id")
    newNo = request.form.to_dict().get("invoice_no")
    updateInvoiceNo(branchId, newNo)
    return jsonify({"success": True, "message": "Invoice Updated"})

@app.route("/newsetPaid", methods=["PATCH"])
def setPaid():
    amount = request.form.to_dict().get("amount")
    plan = request.form.to_dict().get("plan")
    email = request.form.to_dict().get("email")
    branchId = request.form.to_dict().get("branch_id")
    newsetPaid(plan, email, branchId, amount)
    return jsonify({"success": True, "message": "Activated"})

@app.route("/getCurrentCompany", methods=["POST"])
def getCurrentCompany():
        data = request.get_json()
        branchId = data.get("branch")
        return getCurrentCompany(branchId)

@app.route("/getAllMyBranches", methods=["POST"])
def getAllMyBranches():
        data = request.get_json()
        companyId = data.get("branch")
        return getAllMyBranches(companyId)

@app.route("/branchSubscription", methods=["POST"])
def getsubscriptionStatus():
    data = request.get_json()
    branchId = data.get("branch_id")

    return subscriptionStatus(branchId)

@app.route("/createShift", methods=["POST"])
def newcreateShift():
        data = request.get_json()
        branchId = data.get("branch_id")
        sdate = data.get("sdate"),
        shift_description = data.get("shift_description"),
        till_id = data.get("till_id")
        createShift(branchId, sdate, shift_description, till_id)
        return jsonify({"success": True, "message": "Shift created"})



@app.route("/getRunningShift", methods=["POST"])
def newgetRunningShift():
        data = request.get_json()
        branch_id = data.get("branch")
        print(branch_id)
        return getRunningShift(branch_id)

@app.route("/getExpenses", methods=["POST"])
def getMyallExpenses():
        data = request.get_json()
        branch_id = data.get("branch")
        print(branch_id)
        return getmyExpenses(branch_id)


@app.route("/getShiftsExpenses", methods=["POST"])
def getShiftsExpenses():
    data = request.get_json()
    branch_id = data.get("branch")
    cash_amount = data.get("amount")
    pay_date = data.get("date")
    pay_description = data.get("desc")
    pay_ref = data.get("ref")
    pay_to = data.get("to")
    shift_id = data.get("shift")
    till_id = data.get("till")
    ShiftsExpenses(branch_id, cash_amount, pay_date, pay_description, pay_ref, pay_to, shift_id, till_id)
    return jsonify({"success": True, "message": "Expense Added"})

@app.route("/addPosReceiptDetails", methods=["POST"])
def newaddPosReceiptDetails():
    data = request.get_json()
    branch_id = data.get("branch_id")
    cartItem = data.get("item_printed")
    receipt_id = data.get("receipt_id")
    location = data.get("location")
    code = data.get("uom_code")
    staff_id = data.get("staff_id")
    shift_id = data.get("shift_id")
    till_id = data.get("till_id")
    receipt_total_amount = data.get("receipt_total_amount")
    addPosReceiptDetails(branch_id,cartItem,receipt_id,location,code, staff_id,shift_id,till_id, receipt_total_amount,)
    return jsonify({"success": True, "message": "Receipt of POS Added"})


@app.route("/checkout", methods=["POST"])
def getCheckout():
    data = request.get_json()

    branch_id = data.get("branch_id")
    total = data.get("receipt_total_amount")
    cash = data.get("receipt_cash_amount")
    mpesa = data.get("receipt_mobile_money")
    bank = data.get("receipt_bank_amount")
    shift_id = data.get("shift_id")
    till_id = data.get("till_id")
    customerId = data.get("customer_id")
    staffId = data.get("staff_id")
    location = data.get("location_id")
    cart = data.get("cart")

    createPosReceipt(branch_id, customerId, location, cash, bank, mpesa, total, shift_id, staffId, till_id, cart)
    return jsonify({"success": True, "message": "Checkout success"})

@app.route("/getBranchSales", methods=["POST"])
def Branchsales():
    data = request.get_json()
    branch_id = data.get("branch")
    return fetchCreatedReceipts(branch_id)

@app.route("/add_Supplier", methods=["POST"])
def newaddSupplier():
    data = request.get_json()
    bank_acc = data.get("supplier_bank_acc")
    name = data.get("supplier_name")
    phone_no = data.get("supplier_phone_no")
    address = data.get("supplier_address")
    pin_number = data.get("supplier_pin")
    branch_id = data.get("branch_id")
    balance = data.get("supplier_running_bal")
    addSupplier(branch_id,bank_acc,address,name,phone_no,balance,pin_number)

    return jsonify({"success": True, "message": "Supplier Added"})

@app.route("/supplier", methods=["POST"])
def getSupplierList():
        data = request.get_json()
        branch_id = data.get("branch")
        print(branch_id)
        return getSupplierList(branch_id)


@app.route("/SupplierStatusChange", methods=["PATCH"])
def SupplierChangeStatus():
    status = request.form.to_dict().get("status")
    customerId = request.form.to_dict().get("id")
    changeSupplierStatus(status, customerId)
    return jsonify({"success": True, "message": "Supplier status Updated"})

@app.route("/updatesSupplier", methods=["PATCH"])
def Supplierupdate():
    bank_acc = request.form.to_dict().get("account")
    name = request.form.to_dict().get("name")
    phone_no = request.form.to_dict().get("phone")
    address = request.form.to_dict().get("address")
    pin_number = request.form.to_dict().get("pin")
    balance = request.form.to_dict().get("balance")
    supplier_id = request.form.to_dict().get("supplierId")
    print("Supplier ID:", supplier_id, "balance:", balance)
    UpdateSupplier(supplier_id,bank_acc, address, name,phone_no,pin_number,balance)
    return jsonify({"success": True, "message": "Supplier Updated"})

@app.route("/getCurrentRunningBalance", methods=["POST"])
def newgetCurrentRunningBalance():
        data = request.get_json()
        branch_id = data.get("branch")
        print(branch_id)
        return getCurrentRunningBalance(branch_id)

@app.route("/updateCurrentRunningBalance", methods=["PATCH"])
def updateRunningBalance():
    supplierId = request.form.to_dict().get("supplier_id")
    amount = request.form.to_dict().get("supplier_running_bal")
    updateCurrentRunningBalance(supplierId, amount)
    return jsonify({"success": True, "message": "Supplier status Updated"})

@app.route("/nawiriaddSupplierPayment", methods=["POST"])
def newaddPayment():
    data = request.get_json()
    branch_id = data.get("branch_id")
    created_by = data.get("created_by")
    created_on = data.get("created_on")
    trans_type_id = data.get("trans_type_id")
    transaction_amount = data.get("transaction_amount")
    transaction_comment = data.get("transaction_comment")
    transaction_ref = data.get("transaction_payment_ref")
    supplierId = data.get("supplier_trans_id")
    nawiriaddPayment(supplierId, branch_id,created_by,created_on,trans_type_id,transaction_amount,transaction_comment,transaction_ref)
    return jsonify({"success": True, "message": "Payment Added"})

@app.route("/getTransactionsBySupplierID", methods=["POST"])
def getSupTran():
    data = request.get_json()
    supplierId = data.get("supplierId")
    return getTransactionList(supplierId)

@app.route("/getSupplierTransFiltered", methods=["POST"])
def getSupplierTransactionFiltered():

    data = request.get_json()

    supplierId = data.get("supplierId")
    fromDate = data.get("from")
    toDate = request.form.to_dict().get("to")
    if fromDate == "":
        return getTransactionListFilteredTo(supplierId, toDate)
    elif toDate == "":
        return getTransactionListFilteredFrom(supplierId, fromDate)
    else:
        return getTransactionListFiltered(supplierId, fromDate, toDate)









# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(port=5000, debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
