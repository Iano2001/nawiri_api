
from django.db import models


class AccessRight(models.Model):
    access_right_id = models.IntegerField(primary_key=True)
    access_right_description = models.CharField(max_length=50, blank=True, null=True)
    active = models.CharField(max_length=1, blank=True, null=True)
    indorder = models.IntegerField(blank=True, null=True)
    posbutton = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'access_right'


class AccessRightModule(models.Model):
    access_right_module_id = models.CharField(primary_key=True, max_length=36)
    access_right = models.ForeignKey(AccessRight, models.DO_NOTHING, blank=True, null=True)
    active = models.CharField(max_length=1, blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    edited_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    edited_on = models.DateTimeField(blank=True, null=True)
    staff_category_id = models.CharField(max_length=36, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'access_right_module'


class AlembicVersion(models.Model):
    version_num = models.CharField(primary_key=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'alembic_version'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BankTrans(models.Model):
    bank_trans_id = models.CharField(primary_key=True, max_length=36)
    bank_id = models.CharField(max_length=36, blank=True, null=True)
    bank_trans_type_id = models.CharField(max_length=36, blank=True, null=True)
    trans_ref = models.CharField(max_length=50, blank=True, null=True)
    trans_date = models.DateTimeField(blank=True, null=True)
    trans_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    trans_running_bal = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    trans_comment = models.CharField(max_length=250, blank=True, null=True)
    trans_complete = models.CharField(max_length=1, blank=True, null=True)
    trans_completed_by = models.CharField(max_length=36, blank=True, null=True)
    trans_completed_on = models.DateTimeField(blank=True, null=True)
    trans_cancelled = models.CharField(max_length=1, blank=True, null=True)
    trans_cancelled_by = models.CharField(max_length=36, blank=True, null=True)
    trans_cancelled_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bank_trans'


class BankTransType(models.Model):
    bank_trans_type_id = models.CharField(primary_key=True, max_length=36)
    bank_trans_type_description = models.CharField(max_length=50, blank=True, null=True)
    bank_trans_type_sign = models.CharField(max_length=1, blank=True, null=True)
    bank_trans_type_count = models.FloatField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    pair_id = models.CharField(max_length=36, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bank_trans_type'


class Banks(models.Model):
    bank_id = models.CharField(primary_key=True, max_length=36)
    bank_acc_no = models.CharField(max_length=50, blank=True, null=True)
    bank_name = models.CharField(max_length=250, blank=True, null=True)
    bank_running_bal = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    total_credit = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    total_debit = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    account_manager = models.CharField(max_length=250, blank=True, null=True)
    account_details = models.CharField(max_length=250, blank=True, null=True)
    active = models.CharField(max_length=1, blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'banks'


class BatchTable(models.Model):
    batch_id = models.CharField(max_length=36, blank=True, null=True)
    batchno = models.TextField(blank=True, null=True)
    batchexpiry = models.DateTimeField(blank=True, null=True)
    batch_quantity = models.BigIntegerField(blank=True, null=True)
    batch_balance = models.BigIntegerField(blank=True, null=True)
    del_ref = models.CharField(max_length=50, blank=True, null=True)
    batch_comment = models.TextField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    edited_by = models.CharField(max_length=36, blank=True, null=True)
    edited_on = models.DateTimeField(blank=True, null=True)
    product_id = models.CharField(max_length=36, blank=True, null=True)
    location_product_id = models.CharField(max_length=36, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    grnref = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'batch_table'


class Bom(models.Model):
    bom_id = models.CharField(primary_key=True, max_length=36)
    parent_location_product_id = models.CharField(max_length=36, blank=True, null=True)
    location_product_id = models.CharField(max_length=36, blank=True, null=True)
    quantity = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bom'


class Bookings(models.Model):
    booking_id = models.CharField(primary_key=True, max_length=36)
    booking_desc = models.CharField(max_length=250, blank=True, null=True)
    booking_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    edited_on = models.DateTimeField(blank=True, null=True)
    edited_by = models.CharField(max_length=36, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bookings'





class Category(models.Model):
    category_id = models.CharField(primary_key=True, max_length=36)
    show_in_pos = models.CharField(max_length=2)
    category_desc = models.CharField(max_length=50, blank=True, null=True)
    category_count = models.IntegerField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    rmargin = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    wmargin = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    category_code = models.CharField(max_length=5, blank=True, null=True)
    category_type = models.CharField(max_length=100, blank=True, null=True)
    sub_group_id = models.CharField(max_length=36, blank=True, null=True)
    category_printer = models.CharField(max_length=36, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class CiSessions(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    timestamp = models.IntegerField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ci_sessions'


class Company(models.Model):
    company_id = models.IntegerField(primary_key=True)
    company_name = models.CharField(max_length=225, blank=True, null=True)
    company_reg_no = models.CharField(max_length=50, blank=True, null=True)
    company_pinno = models.CharField(max_length=225, blank=True, null=True)
    company_vatno = models.CharField(max_length=100, blank=True, null=True)
    company_tel = models.CharField(max_length=225, blank=True, null=True)
    company_town = models.CharField(max_length=100, blank=True, null=True)
    company_county = models.CharField(max_length=100, blank=True, null=True)
    company_address = models.CharField(max_length=100, blank=True, null=True)
    company_shortname = models.CharField(max_length=100, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    nssf_number = models.CharField(max_length=100, blank=True, null=True)
    nhif_number = models.CharField(max_length=100, blank=True, null=True)
    logo = models.TextField(blank=True, null=True)
    payment_details = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company'

class Branch(models.Model):
    branch_id = models.IntegerField(primary_key=True)
    branch_name = models.TextField(blank=True, null=True)
    company_id = models.TextField(blank=True, null=True)
    cat_levy_charged = models.CharField(max_length=1, blank=True, null=True)
    period = models.DateTimeField(blank=True, null=True)
    reprint = models.CharField(max_length=1, blank=True, null=True)
    printcaptain = models.CharField(max_length=1, blank=True, null=True)
    billheader = models.CharField(max_length=1, blank=True, null=True)
    randomnames = models.CharField(max_length=1, blank=True, null=True)
    routetrips = models.CharField(max_length=1, blank=True, null=True)
    string1 = models.IntegerField(blank=True, null=True)
    string2 = models.IntegerField(blank=True, null=True)
    custbalinrct = models.CharField(max_length=1, blank=True, null=True)
    changeqty = models.CharField(max_length=1, blank=True, null=True)
    customertrcpt = models.CharField(max_length=1, blank=True, null=True)
    expdate = models.CharField(max_length=36, blank=True, null=True)
    branchcontact = models.TextField(blank=True, null=True)
    sms_api_key = models.TextField(blank=True, null=True)
    sms_user_name = models.CharField(max_length=50, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    modem_enabled = models.CharField(max_length=1, blank=True, null=True)
    modem_port = models.CharField(max_length=50, blank=True, null=True)
    mpesa = models.CharField(max_length=1, blank=True, null=True)
    wsale = models.CharField(max_length=1, blank=True, null=True)
    postouch = models.CharField(max_length=1, blank=True, null=True)
    mpesaurl = models.CharField(max_length=250, blank=True, null=True)
    courierservices = models.CharField(max_length=1, blank=True, null=True)
    online_sync = models.CharField(max_length=1, blank=True, null=True)
    selforder = models.CharField(max_length=1, blank=True, null=True)
    print_credetails = models.CharField(max_length=1, blank=True, null=True)
    sendsms = models.CharField(max_length=1, blank=True, null=True)
    tallyinter = models.CharField(max_length=1, blank=True, null=True)
    tallyserver = models.TextField(blank=True, null=True)
    hqmac = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'branch'


class BulkSms(models.Model):
    sms_id = models.CharField(primary_key=True, max_length=36)
    bulk_sms_ref = models.TextField(blank=True, null=True)
    sms_to = models.TextField(blank=True, null=True)
    sms_to_name = models.CharField(max_length=250, blank=True, null=True)
    sms_message = models.CharField(max_length=250, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    sms_by = models.CharField(max_length=36, blank=True, null=True)
    sms_on = models.DateTimeField(blank=True, null=True)
    sms_sent = models.CharField(max_length=1, blank=True, null=True)
    sms_sent_on = models.DateTimeField(blank=True, null=True)
    sms_cancelled = models.CharField(max_length=1, blank=True, null=True)
    sms_cancelled_by = models.CharField(max_length=36, blank=True, null=True)
    sms_cancelled_on = models.DateTimeField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bulk_sms'


class CompanyUser(models.Model):
    user_id = models.PositiveIntegerField()
    company_id = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'company_user'


class Courier(models.Model):
    courier_id = models.CharField(max_length=36, blank=True, null=True)
    courier_name = models.CharField(max_length=250, blank=True, null=True)
    courier_running_bal = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    courier_total_credit = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    courier_total_debit = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    supplier_pin = models.CharField(max_length=50, blank=True, null=True)
    supplier_bank_acc = models.CharField(max_length=10, blank=True, null=True)
    supplier_phone_no = models.CharField(max_length=16, blank=True, null=True)
    supplier_address = models.CharField(max_length=50, blank=True, null=True)
    supplier_contact_person = models.CharField(max_length=30, blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    active = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'courier'


class CourierSettings(models.Model):
    courier_setting_id = models.CharField(max_length=36, blank=True, null=True)
    courier_id = models.CharField(max_length=36, blank=True, null=True)
    base_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    base_kg = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    per_extra_kg = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'courier_settings'


class CourierTrans(models.Model):
    courier_trans_id = models.CharField(primary_key=True, max_length=36)
    courier_id = models.CharField(max_length=36, blank=True, null=True)
    courier_setting_id = models.CharField(max_length=36, blank=True, null=True)
    courier_type_id = models.CharField(max_length=36, blank=True, null=True)
    trans_ref = models.CharField(max_length=50, blank=True, null=True)
    trans_date = models.DateTimeField(blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    base_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    extra_kg_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    trans_comment = models.CharField(max_length=250, blank=True, null=True)
    trans_by = models.CharField(max_length=36, blank=True, null=True)
    trans_on = models.DateTimeField(blank=True, null=True)
    trans_cancelled = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    trans_running_bal = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    client_contact = models.CharField(max_length=250, blank=True, null=True)
    client_name = models.CharField(max_length=250, blank=True, null=True)
    destination = models.CharField(max_length=250, blank=True, null=True)
    status_id = models.IntegerField(blank=True, null=True)
    trans_status = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'courier_trans'


class CourierType(models.Model):
    courier_type_id = models.IntegerField(primary_key=True)
    courier_type_name = models.CharField(max_length=250, blank=True, null=True)
    courier_type_sign = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'courier_type'


class Customer(models.Model):
    customer_id = models.CharField(primary_key=True, max_length=36)
    customer_acc = models.CharField(max_length=50, blank=True, null=True)
    customer_name = models.TextField(blank=True, null=True)
    customer_running_bal = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    customer_bank_acc = models.CharField(max_length=20, blank=True, null=True)
    customer_phone_no = models.CharField(max_length=16, blank=True, null=True)
    customer_address = models.CharField(max_length=50, blank=True, null=True)
    customer_contact_person = models.CharField(max_length=50, blank=True, null=True)
    customer_credit_limit = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    active = models.CharField(max_length=1, blank=True, null=True)
    customer_total_credit = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    customer_total_debit = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    route_id = models.CharField(max_length=36, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    credit_period = models.IntegerField(blank=True, null=True)
    credit_status = models.CharField(max_length=250, blank=True, null=True)
    pin_number = models.CharField(max_length=50, blank=True, null=True)
    clearpbalance = models.CharField(max_length=1, blank=True, null=True)
    request_orderno = models.CharField(max_length=1, blank=True, null=True)
    fprint = models.TextField(blank=True, null=True)
    isbranch = models.CharField(max_length=1, blank=True, null=True)
    fbranch = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'


class CustomerOders(models.Model):
    order_id = models.CharField(primary_key=True, max_length=36)
    product_id = models.CharField(max_length=36, blank=True, null=True)
    confirmed = models.CharField(max_length=1)
    cancelled = models.CharField(max_length=1, blank=True, null=True)
    confirmed_by = models.CharField(max_length=36, blank=True, null=True)
    cancelled_by = models.CharField(max_length=36, blank=True, null=True)
    confirmed_date = models.DateTimeField(blank=True, null=True)
    customer_id = models.CharField(db_column='Customer_id', max_length=36, blank=True, null=True)  # Field name made lowercase.
    customer_name = models.TextField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    service_vehicle_id = models.CharField(max_length=36, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_oders'


class CustomerOdersDetails(models.Model):
    order_detail_id = models.CharField(primary_key=True, max_length=36)
    customer_order_id = models.CharField(max_length=36, blank=True, null=True)
    location_product_id = models.CharField(max_length=36)
    product_sp = models.BigIntegerField(blank=True, null=True)
    trans_quantity = models.BigIntegerField()
    cancelled = models.CharField(max_length=1, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    linenum = models.IntegerField(blank=True, null=True)
    uom_code = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_oders_details'


class CustomerTrans(models.Model):
    customer_trans_id = models.CharField(primary_key=True, max_length=36)
    transaction_ref = models.CharField(max_length=50, blank=True, null=True)
    transaction_date = models.DateTimeField(blank=True, null=True)
    transaction_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    transaction_approved = models.CharField(max_length=1, blank=True, null=True)
    customer = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)
    trans_type = models.ForeignKey('TransType', models.DO_NOTHING, blank=True, null=True)
    transaction_comment = models.TextField(blank=True, null=True)
    running_bal = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    trip_id = models.CharField(max_length=36, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    trans_by = models.CharField(max_length=50, blank=True, null=True)
    transaction_vat = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_trans'


class DaySummary(models.Model):
    summary_id = models.CharField(primary_key=True, max_length=36)
    noofshifts = models.IntegerField(blank=True, null=True)
    summary_date = models.DateField(blank=True, null=True)
    time_started = models.TimeField(blank=True, null=True)
    time_ended = models.TimeField(blank=True, null=True)
    day_started_by = models.TextField(blank=True, null=True)
    day_ended_by = models.TextField(blank=True, null=True)
    receipts_total_amount = models.BigIntegerField(blank=True, null=True)
    total_vat = models.BigIntegerField(blank=True, null=True)
    total_cat_levey = models.BigIntegerField(blank=True, null=True)
    total_cash_amount = models.BigIntegerField(blank=True, null=True)
    total_cheque_amount = models.BigIntegerField(blank=True, null=True)
    total_card_amount = models.BigIntegerField(blank=True, null=True)
    total_voucher_amount = models.BigIntegerField(blank=True, null=True)
    total_mobile_money = models.BigIntegerField(blank=True, null=True)
    branch = models.ForeignKey(Branch, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'day_summary'


class DeliveryCustomer(models.Model):
    dcustomer_id = models.CharField(primary_key=True, max_length=36)
    dcustomer_name = models.TextField(blank=True, null=True)
    dcustomer_number = models.CharField(max_length=250, blank=True, null=True)
    dcustomer_details = models.CharField(max_length=250, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    active = models.CharField(max_length=1, blank=True, null=True)
    route_id = models.CharField(max_length=36, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    credit_period = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'delivery_customer'


class DeliveryDetails(models.Model):
    delivery_detail_id = models.CharField(primary_key=True, max_length=36)
    receipt_ref = models.CharField(max_length=50, blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    delivery_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    delivery_paid = models.CharField(max_length=1, blank=True, null=True)
    dcustomer_id = models.CharField(max_length=36, blank=True, null=True)
    delivery_cancelled = models.CharField(max_length=1, blank=True, null=True)
    cancelled_on = models.DateTimeField(blank=True, null=True)
    cancelled_by = models.CharField(max_length=50, blank=True, null=True)
    delivery_comment = models.CharField(max_length=250, blank=True, null=True)
    delivery_location = models.CharField(max_length=50, blank=True, null=True)
    collection_by = models.CharField(max_length=50, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'delivery_details'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Driver(models.Model):
    driver_id = models.CharField(primary_key=True, max_length=36)
    driver_name = models.TextField(blank=True, null=True)
    staff_id = models.CharField(max_length=36, blank=True, null=True)
    licence_no = models.CharField(max_length=50, blank=True, null=True)
    exp_date = models.DateTimeField(blank=True, null=True)
    staff = models.CharField(max_length=1, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    active = models.CharField(max_length=1, blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'driver'


class FailedJobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=255)
    connection = models.TextField()
    queue = models.TextField()
    payload = models.TextField()
    exception = models.TextField()
    failed_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'failed_jobs'


class Fleet(models.Model):
    vehicle_id = models.CharField(primary_key=True, max_length=36)
    plate_no = models.CharField(max_length=50, blank=True, null=True)
    serial_no = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    make = models.CharField(max_length=50, blank=True, null=True)
    manufacture_year = models.DateTimeField(blank=True, null=True)
    engine_size = models.CharField(max_length=50, blank=True, null=True)
    purchase_date = models.DateTimeField(blank=True, null=True)
    identification = models.CharField(max_length=50, blank=True, null=True)
    fleet_owner_id = models.CharField(max_length=36, blank=True, null=True)
    transmission_type = models.CharField(max_length=50, blank=True, null=True)
    fuel_type = models.CharField(max_length=50, blank=True, null=True)
    current_mileage = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    last_mileage = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    total_mileage = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    total_consumption = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    avarage_consumption = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    active = models.CharField(max_length=1, blank=True, null=True)
    driver_id = models.CharField(max_length=36, blank=True, null=True)
    vehicle_category_id = models.CharField(max_length=36, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    net_weight = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    gross_weight = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    current_value = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    starting_value = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    depreciation = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    salvage_value = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    value_start_date = models.DateTimeField(blank=True, null=True)
    value_current_date = models.DateTimeField(blank=True, null=True)
    value_cycles = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    edited_by = models.CharField(max_length=36, blank=True, null=True)
    edited_on = models.DateTimeField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    vehicle_available = models.CharField(max_length=1, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    leased = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fleet'


class FleetInsuarance(models.Model):
    insuarance_id = models.CharField(primary_key=True, max_length=36)
    insuarance_description = models.CharField(max_length=50, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fleet_insuarance'


class FleetOwner(models.Model):
    fleet_owner_id = models.CharField(primary_key=True, max_length=36)
    fleet_owner_name = models.TextField(blank=True, null=True)
    running_balance = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    total_debit = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    total_credit = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    contacts = models.TextField(blank=True, null=True)
    active = models.CharField(max_length=1, blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fleet_owner'


class FleetTrans(models.Model):
    fleet_trans_id = models.CharField(max_length=36, blank=True, null=True)
    trans_date = models.DateTimeField(blank=True, null=True)
    trans_ref = models.CharField(max_length=50, blank=True, null=True)
    vehicle_id = models.CharField(max_length=36, blank=True, null=True)
    driver_id = models.CharField(max_length=36, blank=True, null=True)
    fleet_trans_type_id = models.CharField(max_length=36, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    quantity = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    completed = models.CharField(max_length=1, blank=True, null=True)
    cancelled = models.CharField(max_length=1, blank=True, null=True)
    completed_by = models.CharField(max_length=36, blank=True, null=True)
    completed_on = models.DateTimeField(blank=True, null=True)
    cancelled_by = models.CharField(max_length=36, blank=True, null=True)
    cancelled_on = models.DateTimeField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    ref_id = models.CharField(max_length=36, blank=True, null=True)
    trans_ref_type = models.CharField(max_length=50, blank=True, null=True)
    running_bal = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    trip_id = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    next_due = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fleet_trans'


class FleetTransType(models.Model):
    fleet_trans_type_id = models.CharField(primary_key=True, max_length=36)
    type_description = models.TextField(blank=True, null=True)
    sign = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fleet_trans_type'


class HsTransFile(models.Model):
    hs_trans_id = models.CharField(primary_key=True, max_length=36)
    trans_date = models.DateTimeField(blank=True, null=True)
    trans_reference = models.CharField(max_length=250, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    trans_type_id = models.IntegerField(blank=True, null=True)
    uom_code = models.CharField(max_length=3, blank=True, null=True)
    trans_quantity = models.BigIntegerField(blank=True, null=True)
    trans_base_quantity = models.BigIntegerField(blank=True, null=True)
    batch_no = models.CharField(max_length=50, blank=True, null=True)
    trans_comment = models.TextField(blank=True, null=True)
    product_id = models.CharField(max_length=36, blank=True, null=True)
    location_product_id = models.CharField(max_length=36, blank=True, null=True)
    complete = models.CharField(max_length=1, blank=True, null=True)
    cancelled = models.CharField(max_length=1, blank=True, null=True)
    supplier_id = models.CharField(max_length=36, blank=True, null=True)
    location_id = models.CharField(max_length=36, blank=True, null=True)
    del_note = models.CharField(max_length=50, blank=True, null=True)
    inv_no = models.CharField(max_length=50, blank=True, null=True)
    lpo_no = models.CharField(max_length=50, blank=True, null=True)
    cost_price = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    track_no = models.CharField(max_length=50, blank=True, null=True)
    tran_discount = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hs_trans_file'


class Insuarance(models.Model):
    insuarance_id = models.CharField(primary_key=True, max_length=36)
    insuarance_name = models.TextField(blank=True, null=True)
    insuarance_address = models.TextField(blank=True, null=True)
    insuarance_contactp = models.CharField(max_length=50, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'insuarance'


class InsuaranceTrans(models.Model):
    insuarance_trans_id = models.CharField(primary_key=True, max_length=36)
    insuarance_trans_ref = models.CharField(max_length=50, blank=True, null=True)
    insuarance_trans_date = models.DateTimeField(blank=True, null=True)
    insuarance_id = models.CharField(max_length=36, blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    cost_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    cancelled = models.CharField(max_length=1, blank=True, null=True)
    cancelled_by = models.CharField(max_length=36, blank=True, null=True)
    cancelled_on = models.DateTimeField(blank=True, null=True)
    company = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    vehicle_id = models.CharField(max_length=36, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'insuarance_trans'


class JobCard(models.Model):
    job_id = models.CharField(primary_key=True, max_length=36)
    supplier_id = models.CharField(max_length=36, blank=True, null=True)
    job_ref = models.CharField(max_length=50, blank=True, null=True)
    job_date = models.DateTimeField(blank=True, null=True)
    process_level = models.IntegerField(blank=True, null=True)
    total_sorting = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    total_crushing = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    sorting_by = models.CharField(max_length=36, blank=True, null=True)
    crushing_by = models.CharField(max_length=36, blank=True, null=True)
    sorting_date = models.DateTimeField(blank=True, null=True)
    crushing_date = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    total_received = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    total_invoice = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    total_payment = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    balance_due = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    cancelled = models.CharField(max_length=1, blank=True, null=True)
    cancelled_by = models.CharField(max_length=36, blank=True, null=True)
    cancelled_on = models.DateTimeField(blank=True, null=True)
    cancel_approved = models.CharField(max_length=1, blank=True, null=True)
    cancel_approved_by = models.CharField(max_length=36, blank=True, null=True)
    cancel_approved_on = models.DateTimeField(blank=True, null=True)
    total_seeds = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    job_open = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job_card'


class JobTrans(models.Model):
    job_trans_id = models.CharField(primary_key=True, max_length=36)
    job_id = models.CharField(max_length=36, blank=True, null=True)
    trans_ref = models.CharField(max_length=50, blank=True, null=True)
    trans_date = models.DateTimeField(blank=True, null=True)
    trans_level = models.IntegerField(blank=True, null=True)
    trans_quantity = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    price_per_unit = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    total_cost = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    trans_by = models.CharField(max_length=36, blank=True, null=True)
    trans_on = models.DateTimeField(blank=True, null=True)
    cancelled = models.CharField(max_length=1, blank=True, null=True)
    cancelled_by = models.CharField(max_length=36, blank=True, null=True)
    cancelled_on = models.DateTimeField(blank=True, null=True)
    cancel_approved = models.CharField(max_length=1, blank=True, null=True)
    cancel_approved_by = models.CharField(max_length=36, blank=True, null=True)
    cancel_approved_on = models.DateTimeField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    location_id = models.CharField(max_length=36, blank=True, null=True)
    quantity_processed = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    quantity_remaining = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job_trans'


class Loans(models.Model):
    loan_id = models.CharField(primary_key=True, max_length=36)
    loan_ref = models.CharField(max_length=50, blank=True, null=True)
    loan_date = models.DateTimeField(blank=True, null=True)
    loan_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    loan_balance = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    installments_number = models.IntegerField(blank=True, null=True)
    loan_installment = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    installments_paid = models.IntegerField(blank=True, null=True)
    loan_interest = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    loan_duration = models.CharField(max_length=50, blank=True, null=True)
    loan_approved = models.CharField(max_length=1, blank=True, null=True)
    loan_cancelled = models.CharField(max_length=1, blank=True, null=True)
    loan_approved_by = models.CharField(max_length=36, blank=True, null=True)
    loan_cancelled_by = models.CharField(max_length=36, blank=True, null=True)
    loan_approval_comments = models.TextField(blank=True, null=True)
    loan_cancelled_comments = models.TextField(blank=True, null=True)
    loan_comments = models.TextField(blank=True, null=True)
    last_installment_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    staff_id = models.CharField(max_length=36, blank=True, null=True)
    loan_start_date = models.DateTimeField(blank=True, null=True)
    loan_end_date = models.DateTimeField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loans'


class Location(models.Model):
    location_id = models.CharField(primary_key=True, max_length=36)
    location_description = models.TextField(blank=True, null=True)
    branch = models.ForeignKey(Branch, models.DO_NOTHING, blank=True, null=True)
    posl = models.TextField(blank=True, null=True)
    remoteprinter = models.CharField(max_length=50, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location'


class LocationStock(models.Model):
    location_product_id = models.CharField(primary_key=True, max_length=36)
    location_product_quantity = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    product = models.ForeignKey('StockF', models.DO_NOTHING, blank=True, null=True)
    uom_code = models.TextField(blank=True, null=True)
    location_product_max_quantity = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    location_product_min_quantity = models.BigIntegerField(blank=True, null=True)
    location = models.ForeignKey(Location, models.DO_NOTHING, blank=True, null=True)
    location_product_reorder_level = models.BigIntegerField(blank=True, null=True)
    location_productcode = models.CharField(max_length=10, blank=True, null=True)
    location_product_scancode = models.CharField(max_length=20, blank=True, null=True)
    location_product_description = models.TextField(blank=True, null=True)
    location_product_sp = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    location_product_vattable = models.CharField(max_length=1, blank=True, null=True)
    fixed_price = models.CharField(max_length=1, blank=True, null=True)
    category_id = models.CharField(max_length=36, blank=True, null=True)
    # location_product_catlv = models.CharField(max_length=1, blank=True, null=True)
    location_product_sp1 = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    product_image = models.TextField(blank=True, null=True)
    accompaniments = models.TextField(blank=True, null=True)
    partaccompaniment = models.IntegerField(blank=True, null=True)
    batch_tracking = models.CharField(max_length=1, blank=True, null=True)
    blockneg = models.CharField(max_length=1, blank=True, null=True)
    active = models.CharField(max_length=1, blank=True, null=True)
    service = models.CharField(max_length=1, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    packaging_uom = models.CharField(max_length=3, blank=True, null=True)
    packaging_qty = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    packaging_fixed = models.CharField(max_length=1, blank=True, null=True)
    packaging_ratio = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    fuelvat = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location_stock'


class LoyatyCustomer(models.Model):
    loyaty_customer_id = models.CharField(primary_key=True, max_length=36)
    loyaty_customer_sir_name = models.CharField(max_length=250, blank=True, null=True)
    loyaty_customer_o_names = models.CharField(max_length=250, blank=True, null=True)
    loyaty_customer_nid = models.CharField(max_length=20, blank=True, null=True)
    loyaty_customer_phone = models.CharField(max_length=20, blank=True, null=True)
    loyaty_customer_points = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    loyaty_customer_accured = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    loyaty_customer_redeemed = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    loyaty_customer_active = models.CharField(max_length=1, blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loyaty_customer'


class LoyatyCustomerParameter(models.Model):
    loyaty_customer_para_id = models.CharField(primary_key=True, max_length=36)
    per_point_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    minimum_receipt_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    round_off = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    redeem_point_value = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    redeem_active = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=10, blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loyaty_customer_parameter'


class LoyatyCustomerTrans(models.Model):
    loyaty_customer_trans_id = models.CharField(primary_key=True, max_length=36)
    trans_date = models.DateTimeField(blank=True, null=True)
    trans_ref = models.CharField(max_length=50, blank=True, null=True)
    loyaty_customer_id = models.CharField(max_length=36, blank=True, null=True)
    loyaty_customer_trans_type_id = models.IntegerField(blank=True, null=True)
    per_point_factor = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    trans_points = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    running_bal = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    cancelled = models.CharField(max_length=1, blank=True, null=True)
    cancelled_on = models.DateTimeField(blank=True, null=True)
    cancelled_by = models.CharField(max_length=36, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loyaty_customer_trans'


class LoyatyCustomerTransType(models.Model):
    loyaty_customer_trans_type_id = models.IntegerField(primary_key=True)
    loyaty_customer_trans_type_desc = models.CharField(max_length=250, blank=True, null=True)
    loyaty_customer_trans_type_sign = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loyaty_customer_trans_type'


class MachineList(models.Model):
    machine_id = models.CharField(primary_key=True, max_length=36)
    machine_name = models.CharField(max_length=250, blank=True, null=True)
    machine_ip = models.CharField(max_length=50, blank=True, null=True)
    machine_connected = models.CharField(max_length=1, blank=True, null=True)
    last_connect = models.DateTimeField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    machine_allowed = models.CharField(max_length=1, blank=True, null=True)
    machine_pos = models.CharField(max_length=1, blank=True, null=True)
    machine_backoffice = models.CharField(max_length=1, blank=True, null=True)
    machine_cashier = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'machine_list'


class Migrations(models.Model):
    migration = models.CharField(max_length=255)
    batch = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'migrations'


class Mileage(models.Model):
    mileage_id = models.CharField(max_length=36, blank=True, null=True)
    mileage_date = models.DateTimeField(blank=True, null=True)
    trip_id = models.CharField(max_length=36, blank=True, null=True)
    last_mileage = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    current_mileage = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    vehicle_id = models.CharField(max_length=36, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mileage'


class MmSms(models.Model):
    sms_id = models.CharField(primary_key=True, max_length=36)
    sms_number = models.CharField(max_length=50, blank=True, null=True)
    sms_mm_ref = models.CharField(unique=True, max_length=50, blank=True, null=True)
    sms_client = models.CharField(max_length=250, blank=True, null=True)
    sms_client_number = models.CharField(max_length=250, blank=True, null=True)
    sms_content = models.CharField(max_length=250, blank=True, null=True)
    sms_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    sms_date = models.DateTimeField(blank=True, null=True)
    sms_credited = models.CharField(max_length=1, blank=True, null=True)
    sms_used = models.CharField(max_length=1, blank=True, null=True)
    sms_receipt_ref = models.CharField(max_length=250, blank=True, null=True)
    sms_type = models.CharField(max_length=10, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    cancelled = models.CharField(max_length=1, blank=True, null=True)
    cancelled_by = models.CharField(max_length=36, blank=True, null=True)
    cancelled_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mm_sms'


class Modules(models.Model):
    module_id = models.IntegerField(primary_key=True)
    module_description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'modules'


class MonthlyRoll(models.Model):
    monthly_roll_id = models.CharField(primary_key=True, max_length=36)
    monthly_roll_date = models.DateTimeField(blank=True, null=True)
    monthly_roll_period = models.DateTimeField(blank=True, null=True)
    staff_id = models.CharField(max_length=36, blank=True, null=True)
    gross_pay = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    paye = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    nssf1 = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    nssf2 = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    nhif = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    loan_deduction = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    net_pay = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    noncashbenefit = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    allowable_deductions = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    taxable_pay = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    roll_by = models.CharField(max_length=36, blank=True, null=True)
    roll_cancelled = models.CharField(max_length=1, blank=True, null=True)
    roll_complete = models.CharField(max_length=1, blank=True, null=True)
    advancepayment = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    insuarance_relief = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'monthly_roll'


class NhifRates(models.Model):
    rate_id = models.IntegerField(primary_key=True)
    rate_lower_limit = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    rate_upper_limit = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    deduction = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nhif_rates'


class NssfRates(models.Model):
    nssf_rate_id = models.IntegerField(primary_key=True)
    limit_lower_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    limit_upper_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    tier1 = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    tier2 = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nssf_rates'


class Ozekimessagein(models.Model):
    id = models.IntegerField(primary_key=True)
    sender = models.CharField(max_length=30, blank=True, null=True)
    receiver = models.CharField(max_length=30, blank=True, null=True)
    msg = models.TextField(blank=True, null=True)
    senttime = models.CharField(max_length=100, blank=True, null=True)
    receivedtime = models.CharField(max_length=100, blank=True, null=True)
    operator = models.CharField(max_length=30, blank=True, null=True)
    msgtype = models.CharField(max_length=30, blank=True, null=True)
    reference = models.CharField(max_length=30, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ozekimessagein'


class Ozekimessageout(models.Model):
    id = models.IntegerField(primary_key=True)
    sender = models.CharField(max_length=30, blank=True, null=True)
    receiver = models.CharField(max_length=30, blank=True, null=True)
    msg = models.CharField(max_length=160, blank=True, null=True)
    senttime = models.CharField(max_length=100, blank=True, null=True)
    receivedtime = models.CharField(max_length=100, blank=True, null=True)
    operator = models.CharField(max_length=100, blank=True, null=True)
    msgtype = models.CharField(max_length=30, blank=True, null=True)
    reference = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    errormsg = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ozekimessageout'


class ParameterFile(models.Model):
    parameter_id = models.CharField(primary_key=True, max_length=36)
    branch_id = models.IntegerField(blank=True, null=True)
    lpo_no = models.IntegerField(blank=True, null=True)
    quote_no = models.IntegerField(blank=True, null=True)
    invoice_no = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    expence_no = models.IntegerField(blank=True, null=True)
    rmargin = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    wmargin = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    foliono = models.IntegerField(blank=True, null=True)
    customerno = models.IntegerField(blank=True, null=True)
    supplierno = models.IntegerField(blank=True, null=True)
    grn_no = models.IntegerField(blank=True, null=True)
    fscan = models.CharField(max_length=1, blank=True, null=True)
    categoryno = models.IntegerField(blank=True, null=True)
    jobno = models.IntegerField(blank=True, null=True)
    staffno = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parameter_file'


class PasswordResets(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'password_resets'


class PayOut(models.Model):
    pay_id = models.CharField(primary_key=True, max_length=36)
    pay_date = models.DateField(blank=True, null=True)
    pay_time = models.TimeField(blank=True, null=True)
    pay_to = models.TextField(blank=True, null=True)
    staff_id = models.CharField(max_length=36, blank=True, null=True)
    pay_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    pay_type_id = models.IntegerField(blank=True, null=True)
    shift_id = models.CharField(max_length=36, blank=True, null=True)
    cash_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    cc_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    voucher_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    pay_description = models.CharField(max_length=225, blank=True, null=True)
    cheque_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    mobile_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    customer_id = models.CharField(max_length=36, blank=True, null=True)
    till_id = models.CharField(max_length=36, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    f_id = models.CharField(max_length=36, blank=True, null=True)
    pay_ref = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pay_out'


class PayTrans(models.Model):
    pay_trans_id = models.CharField(primary_key=True, max_length=36)
    pay_trans_ref = models.CharField(max_length=50, blank=True, null=True)
    pay_trans_type_id = models.IntegerField(blank=True, null=True)
    pay_trans_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    pay_trans_date = models.DateTimeField(blank=True, null=True)
    pay_trans_by = models.CharField(max_length=36, blank=True, null=True)
    pay_trans_on = models.DateTimeField(blank=True, null=True)
    pay_trans_run_bal = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    pay_trans_cancelled = models.CharField(max_length=1, blank=True, null=True)
    pay_trans_period = models.DateTimeField(blank=True, null=True)
    pay_trans_approved = models.CharField(max_length=1, blank=True, null=True)
    staff_id = models.CharField(max_length=36, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pay_trans'


class PayTransType(models.Model):
    pay_trans_type_id = models.IntegerField(primary_key=True)
    pay_trans_type_desc = models.CharField(max_length=250, blank=True, null=True)
    pay_trans_type_sign = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pay_trans_type'


class PayType(models.Model):
    pay_type_id = models.IntegerField(primary_key=True)
    pay_type_desc = models.CharField(max_length=50, blank=True, null=True)
    pay_type_action = models.CharField(max_length=10, blank=True, null=True)
    pay_type_include_zed = models.CharField(max_length=1, blank=True, null=True)
    showbo = models.CharField(max_length=1, blank=True, null=True)
    showfo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pay_type'


class PayeRates(models.Model):
    paye_rate_id = models.IntegerField(primary_key=True)
    limit_lower_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    limit_upper_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    limit_percentage = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'paye_rates'


class PaymentPlan(models.Model):
    payment_plan_id = models.CharField(primary_key=True, max_length=36)
    plan_date = models.DateTimeField(blank=True, null=True)
    supplier_id = models.CharField(max_length=36, blank=True, null=True)
    plan_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    paid = models.CharField(max_length=1, blank=True, null=True)
    trans_id = models.CharField(max_length=36, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    advance = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payment_plan'


class PersonalAccessTokens(models.Model):
    id = models.BigAutoField(primary_key=True)
    tokenable_type = models.CharField(max_length=255)
    tokenable_id = models.PositiveBigIntegerField()
    name = models.CharField(max_length=255)
    token = models.CharField(unique=True, max_length=64)
    abilities = models.TextField(blank=True, null=True)
    last_used_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'personal_access_tokens'


class PosReceipts(models.Model):
    receipt_id = models.CharField(primary_key=True, max_length=36)
    receipt_ref = models.TextField(blank=True, null=True)
    receipt_date = models.DateField(blank=True, null=True)
    receipt_time = models.TimeField(blank=True, null=True)
    receipt_total_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    total_vat = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    total_cat_levy = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    receipt_cash_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    receipt_cheque_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    receipt_card_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    receipt_voucher_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    receipt_mobile_money = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    branch = models.ForeignKey(Branch, models.DO_NOTHING, blank=True, null=True)
    location = models.ForeignKey(Location, models.DO_NOTHING, blank=True, null=True)
    staff = models.ForeignKey('SysUser', models.DO_NOTHING, blank=True, null=True)
    till = models.ForeignKey('Till', models.DO_NOTHING, blank=True, null=True)
    shift = models.ForeignKey('Shift', models.DO_NOTHING, blank=True, null=True)
    cancelled = models.CharField(max_length=1, blank=True, null=True)
    table_id = models.CharField(max_length=36, blank=True, null=True)
    customer = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)
    receipt_paid = models.CharField(max_length=1, blank=True, null=True)
    customer_alias = models.TextField(blank=True, null=True)
    stype = models.TextField(blank=True, null=True)
    dlocation = models.TextField(blank=True, null=True)
    sales_staff_id = models.CharField(max_length=36, blank=True, null=True)
    receipt_code = models.CharField(max_length=50, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    receipt_discount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    uom_code = models.CharField(max_length=3, blank=True, null=True)
    bill_printed = models.CharField(max_length=1, blank=True, null=True)
    total_fuel_vat = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    service_customer_id = models.CharField(max_length=36, blank=True, null=True)
    service_vehicle_id = models.CharField(max_length=36, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pos_receipts'

class PosReceiptDetails(models.Model):
    receipt_details_id = models.CharField(primary_key=True, max_length=36)
    receipt_id = models.CharField(max_length=36, blank=True, null=True)
    # location_product = models.ForeignKey(LocationStock, models.DO_NOTHING, blank=True, null=True)
    # trans_quantity = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    location_product_id = models.CharField(max_length=36, blank=True, null=True)
    trans_quantity = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    product_sp = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    product_bp = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    vat = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    cat_levy = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    cancelled = models.CharField(max_length=1, blank=True, null=True)
    footnote = models.CharField(max_length=50, blank=True, null=True)
    accompaniment_id = models.TextField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    linenum = models.IntegerField(blank=True, null=True)
    uom_code = models.CharField(max_length=3, blank=True, null=True)
    item_printed = models.CharField(max_length=1, blank=True, null=True)
    batch_no = models.TextField(blank=True, null=True)
    fuel_vat = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    discount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    packaging = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pos_receipt_details'

class PosReceiptPayment(models.Model):
    pos_receipt_payment_id = models.CharField(primary_key=True, max_length=36)
    receipt_id = models.CharField(max_length=36, blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    staff_id = models.CharField(max_length=36, blank=True, null=True)
    shift_id = models.CharField(max_length=36, blank=True, null=True)
    till_id = models.CharField(max_length=36, blank=True, null=True)
    cancelled = models.CharField(max_length=1, blank=True, null=True)
    cancelled_by = models.IntegerField(blank=True, null=True)
    cancelled_on = models.DateTimeField(blank=True, null=True)
    payment_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pos_receipt_payment'


class ProcessTable(models.Model):
    process_id = models.CharField(primary_key=True, max_length=36)
    process_name = models.CharField(max_length=50, blank=True, null=True)
    process_price = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    process_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'process_table'


class Promotion(models.Model):
    promotion_id = models.CharField(primary_key=True, max_length=36)
    promotion_description = models.CharField(max_length=250, blank=True, null=True)
    promotion_quantity = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    promotion_price = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    promotion_uom = models.CharField(max_length=3, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    promotion_days = models.CharField(max_length=50, blank=True, null=True)
    promotion_created_by = models.CharField(max_length=36, blank=True, null=True)
    promotion_created_on = models.DateTimeField(blank=True, null=True)
    promotion_updated_by = models.CharField(max_length=36, blank=True, null=True)
    promotion_updated_on = models.DateTimeField(blank=True, null=True)
    promotion_deleted = models.CharField(max_length=1, blank=True, null=True)
    promotion_deleted_by = models.CharField(max_length=36, blank=True, null=True)
    promotion_deleted_on = models.DateTimeField(blank=True, null=True)
    product_id = models.CharField(max_length=36, blank=True, null=True)
    start_time = models.CharField(max_length=50, blank=True, null=True)
    end_time = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'promotion'


class Register(models.Model):
    register_id = models.CharField(primary_key=True, max_length=36)
    register_date = models.DateTimeField(blank=True, null=True)
    staff_id = models.CharField(max_length=36, blank=True, null=True)
    register_by = models.CharField(max_length=36, blank=True, null=True)
    register_on = models.DateTimeField(blank=True, null=True)
    register_cancelled = models.CharField(max_length=1, blank=True, null=True)
    register_type_id = models.IntegerField(blank=True, null=True)
    clock_in = models.DateTimeField(blank=True, null=True)
    clock_out = models.DateTimeField(blank=True, null=True)
    confirmed_by = models.CharField(max_length=36, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'register'


class RegisterType(models.Model):
    register_type_id = models.IntegerField(primary_key=True)
    register_type_description = models.CharField(max_length=250, blank=True, null=True)
    register_type_sign = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'register_type'


class Repack(models.Model):
    repack_id = models.CharField(primary_key=True, max_length=36)
    repark_base_product_id = models.CharField(max_length=36, blank=True, null=True)
    repark_to_product_id = models.CharField(max_length=36, blank=True, null=True)
    convertion_rate = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'repack'


class RepackItems(models.Model):
    repack_item_id = models.CharField(primary_key=True, max_length=36)
    repack_id = models.CharField(max_length=36, blank=True, null=True)
    product_id = models.CharField(max_length=36, blank=True, null=True)
    quantity = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    active = models.CharField(max_length=1, blank=True, null=True)
    qvariable = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'repack_items'


class RepackTrans(models.Model):
    repack_trans_id = models.CharField(primary_key=True, max_length=36)
    repack_id = models.CharField(max_length=36, blank=True, null=True)
    repark_trans_ref = models.CharField(max_length=50, blank=True, null=True)
    repark_trans_date = models.DateTimeField(blank=True, null=True)
    convertion_rate = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    base_qty = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    total_qty = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    repark_by = models.CharField(max_length=36, blank=True, null=True)
    repark_date = models.DateTimeField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'repack_trans'


class RepairMaster(models.Model):
    repair_id = models.CharField(primary_key=True, max_length=36)
    repair_ref = models.CharField(max_length=250, blank=True, null=True)
    order_no = models.CharField(max_length=250, blank=True, null=True)
    uid = models.CharField(max_length=255, blank=True, null=True)
    supplier = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    sp_comm = models.FloatField(blank=True, null=True)
    item_desc = models.CharField(max_length=255, blank=True, null=True)
    comments = models.CharField(max_length=255, blank=True, null=True)
    spare_cost = models.FloatField(blank=True, null=True)
    labour_cost = models.FloatField(blank=True, null=True)
    depreciation = models.FloatField(blank=True, null=True)
    final_settlement = models.FloatField(blank=True, null=True)
    replaced_item = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    service_centre = models.CharField(max_length=255, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    repair_type_id = models.IntegerField(blank=True, null=True)
    master_date = models.DateTimeField(blank=True, null=True)
    actual_spare_cost = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    actual_labour_cost = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    push_inventory = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'repair_master'


class RepairTrans(models.Model):
    repair_trans_id = models.CharField(primary_key=True, max_length=36)
    repair_id = models.CharField(max_length=36, blank=True, null=True)
    repair_trans_date = models.DateTimeField(blank=True, null=True)
    secondary_name = models.CharField(max_length=250, blank=True, null=True)
    secondary_contact = models.CharField(max_length=250, blank=True, null=True)
    item_status = models.CharField(max_length=250, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    trans_by = models.CharField(max_length=36, blank=True, null=True)
    labour_cost = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    spare_cost = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    return_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'repair_trans'


class RepairType(models.Model):
    repair_type_id = models.IntegerField(primary_key=True)
    repair_type_name = models.CharField(max_length=250, blank=True, null=True)
    repair_type_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'repair_type'


class RoomBookingType(models.Model):
    room_booking_type_id = models.CharField(max_length=36, blank=True, null=True)
    room_booking_type_description = models.CharField(max_length=250, blank=True, null=True)
    room_booking_type_charge = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    room_booking_type_by = models.CharField(max_length=36, blank=True, null=True)
    room_booking_type_on = models.DateTimeField(blank=True, null=True)
    room_booking_type_active = models.CharField(max_length=1, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room_booking_type'


class RoomCategory(models.Model):
    room_category_id = models.CharField(primary_key=True, max_length=36)
    room_category_description = models.CharField(max_length=250, blank=True, null=True)
    room_category_available = models.BigIntegerField(blank=True, null=True)
    room_category_occupied = models.BigIntegerField(blank=True, null=True)
    room_category_booked = models.BigIntegerField(blank=True, null=True)
    room_category_reserved = models.BigIntegerField(blank=True, null=True)
    room_category_count = models.BigIntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    edited_by = models.CharField(max_length=36, blank=True, null=True)
    edited_on = models.DateTimeField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    room_category_pax = models.IntegerField(blank=True, null=True)
    room_category_desc = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room_category'


class RoomCustomer(models.Model):
    room_customer_id = models.CharField(primary_key=True, max_length=36)
    customer_names = models.TextField()
    customer_running_bal = models.BigIntegerField()
    customer_idno = models.CharField(max_length=250, blank=True, null=True)
    customer_otherid = models.CharField(max_length=250, blank=True, null=True)
    customer_phone_no = models.CharField(max_length=16, blank=True, null=True)
    customer_address = models.CharField(max_length=50, blank=True, null=True)
    customer_contact_person = models.CharField(db_column='Customer_contact_person', max_length=50, blank=True, null=True)  # Field name made lowercase.
    customer_credit_limit = models.BigIntegerField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    active = models.CharField(max_length=1, blank=True, null=True)
    customer_total_credit = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    customer_total_debit = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room_customer'


class RoomFloor(models.Model):
    room_floor_id = models.CharField(primary_key=True, max_length=36)
    room_floor_description = models.CharField(max_length=250, blank=True, null=True)
    room_floor_available = models.BigIntegerField(blank=True, null=True)
    room_floor_occupied = models.BigIntegerField(blank=True, null=True)
    room_floor_booked = models.BigIntegerField(blank=True, null=True)
    room_floor_reserved = models.BigIntegerField(blank=True, null=True)
    room_category_count = models.BigIntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    edited_by = models.CharField(max_length=36, blank=True, null=True)
    edited_on = models.DateTimeField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room_floor'


class RoomService(models.Model):
    room_service_id = models.CharField(primary_key=True, max_length=36)
    room_service_description = models.CharField(max_length=250, blank=True, null=True)
    room_service_type_id = models.CharField(max_length=36)
    room_service_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    edited_by = models.CharField(max_length=36, blank=True, null=True)
    edited_on = models.DateTimeField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room_service'


class RoomServiceCategory(models.Model):
    room_service_category_id = models.CharField(primary_key=True, max_length=36)
    room_service_category_description = models.CharField(max_length=250, blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room_service_category'


class RoomServiceType(models.Model):
    room_service_type_id = models.CharField(primary_key=True, max_length=36)
    room_service_type_description = models.CharField(max_length=250, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    edited_by = models.CharField(max_length=36, blank=True, null=True)
    edited_on = models.DateTimeField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room_service_type'


class RoomStatus(models.Model):
    room_status_id = models.IntegerField(blank=True, null=True)
    room_status_desc = models.CharField(max_length=250, blank=True, null=True)
    room_status_available = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room_status'


class RoomTrans(models.Model):
    room_trans_id = models.CharField(primary_key=True, max_length=36)
    room_trans_type_id = models.IntegerField()
    room_trans_ref = models.TextField(blank=True, null=True)
    room_trans_date = models.DateTimeField()
    room_trans_quantity = models.BigIntegerField(blank=True, null=True)
    room_trans_unit_price = models.BigIntegerField(blank=True, null=True)
    room_trans_total_amount = models.BigIntegerField(blank=True, null=True)
    total_vat = models.BigIntegerField(blank=True, null=True)
    total_cat_levy = models.BigIntegerField(blank=True, null=True)
    room_trans_cash_amount = models.BigIntegerField(blank=True, null=True)
    room_trans_cheque_amount = models.BigIntegerField(blank=True, null=True)
    room_trans_card_amount = models.BigIntegerField(blank=True, null=True)
    room_trans_voucher_amount = models.BigIntegerField(blank=True, null=True)
    room_trans_mobile_money = models.BigIntegerField(blank=True, null=True)
    room_trans_discount = models.BigIntegerField(blank=True, null=True)
    branch_id = models.IntegerField()
    room_id = models.IntegerField()
    staff_id = models.CharField(max_length=36)
    shift_id = models.CharField(max_length=36, blank=True, null=True)
    completed = models.CharField(max_length=1, blank=True, null=True)
    cancelled = models.CharField(max_length=1, blank=True, null=True)
    room_customer_id = models.IntegerField(blank=True, null=True)
    room_trans_paid = models.CharField(max_length=1, blank=True, null=True)
    customer_alias = models.TextField(blank=True, null=True)
    sales_staff_id = models.IntegerField(db_column='Sales_staff_id', blank=True, null=True)  # Field name made lowercase.
    room_trans_code = models.CharField(max_length=50, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room_trans'


class RoomTransDetails(models.Model):
    room_trans_details_id = models.CharField(primary_key=True, max_length=36)
    room_trans_id = models.CharField(max_length=36, blank=True, null=True)
    room_trans_details_desc = models.TextField(blank=True, null=True)
    room_trans_type_id = models.CharField(max_length=36, blank=True, null=True)
    room_service_id = models.CharField(max_length=36, blank=True, null=True)
    trans_quantity = models.BigIntegerField(blank=True, null=True)
    unit_price = models.BigIntegerField(blank=True, null=True)
    total_amount = models.BigIntegerField(blank=True, null=True)
    vat = models.BigIntegerField(blank=True, null=True)
    cat_levy = models.BigIntegerField(blank=True, null=True)
    cancelled = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room_trans_details'


class RoomTransType(models.Model):
    room_trans_type_id = models.IntegerField(primary_key=True)
    room_trans_type_desc = models.CharField(max_length=250, blank=True, null=True)
    room_trans_type_sign = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room_trans_type'


class Rooms(models.Model):
    room_id = models.CharField(primary_key=True, max_length=36)
    room_ref = models.CharField(max_length=250, blank=True, null=True)
    room_desc = models.CharField(max_length=250, blank=True, null=True)
    room_status_id = models.IntegerField(blank=True, null=True)
    room_created_by = models.CharField(max_length=36, blank=True, null=True)
    room_created_on = models.DateTimeField(blank=True, null=True)
    room_edited_by = models.CharField(max_length=36, blank=True, null=True)
    room_edited_on = models.DateTimeField(blank=True, null=True)
    room_category_id = models.CharField(max_length=36, blank=True, null=True)
    room_floor_id = models.CharField(max_length=36, blank=True, null=True)
    room_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rooms'


class Routes(models.Model):
    route_id = models.CharField(max_length=36)
    branch_id = models.IntegerField(blank=True, null=True)
    route_description = models.TextField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    surcharge = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    route_message = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'routes'


class SaleType(models.Model):
    sale_type_id = models.IntegerField(primary_key=True)
    sale_type_description = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sale_type'


class SalesProcess(models.Model):
    sales_process_id = models.CharField(primary_key=True, max_length=36)
    sales_process_ref = models.CharField(max_length=50, blank=True, null=True)
    trans_ref = models.CharField(max_length=50, blank=True, null=True)
    sales_process_date = models.DateTimeField(blank=True, null=True)
    account_ref = models.CharField(max_length=36, blank=True, null=True)
    exipry_date = models.DateTimeField(blank=True, null=True)
    sale_type_id = models.IntegerField(blank=True, null=True)
    sales_process_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    sales_process_complete = models.CharField(max_length=1, blank=True, null=True)
    sales_process_cancelled = models.CharField(max_length=1, blank=True, null=True)
    cancelled_by = models.CharField(max_length=36, blank=True, null=True)
    cancelled_date = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    sales_process_quantity = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    sales_process_delivered = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    sales_process_vat = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    primary_ref = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sales_process'


class SalesTrans(models.Model):
    sales_trans_id = models.CharField(primary_key=True, max_length=36)
    sales_process_id = models.CharField(max_length=36, blank=True, null=True)
    pos_receipt_id = models.CharField(max_length=36, blank=True, null=True)
    item_description = models.TextField(blank=True, null=True)
    quantity = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    complete = models.CharField(max_length=1, blank=True, null=True)
    cancelled = models.CharField(max_length=1, blank=True, null=True)
    cancelled_by = models.CharField(max_length=36, blank=True, null=True)
    cancelled_date = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sales_trans'


class ServiceCentre(models.Model):
    service_id = models.CharField(primary_key=True, max_length=36)
    job_number = models.CharField(max_length=250, blank=True, null=True)
    customer_id = models.CharField(max_length=36, blank=True, null=True)
    service_date = models.DateTimeField(blank=True, null=True)
    service_advisor = models.CharField(max_length=250, blank=True, null=True)
    order_no = models.CharField(max_length=250, blank=True, null=True)
    contact_person = models.CharField(max_length=250, blank=True, null=True)
    phone_no = models.CharField(max_length=250, blank=True, null=True)
    check_in_notes = models.TextField(blank=True, null=True)
    job_close_notes = models.TextField(blank=True, null=True)
    job_closed = models.CharField(max_length=1, blank=True, null=True)
    job_closed_date = models.DateTimeField(blank=True, null=True)
    job_closed_by = models.CharField(max_length=36, blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    kilometer = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    confirmed_by = models.CharField(max_length=250, blank=True, null=True)
    confirmed = models.CharField(max_length=1, blank=True, null=True)
    confirmed_on = models.DateTimeField(blank=True, null=True)
    job_total = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    service_vehicle_id = models.CharField(max_length=36, blank=True, null=True)
    technician = models.TextField(blank=True, null=True)
    service_customer_id = models.CharField(max_length=36, blank=True, null=True)
    gate_pass = models.CharField(max_length=1, blank=True, null=True)
    gate_pass_on = models.DateTimeField(blank=True, null=True)
    gate_pass_by = models.CharField(max_length=36, blank=True, null=True)
    gate_pass_notes = models.TextField(blank=True, null=True)
    gate_pass_cleared_by = models.CharField(max_length=250, blank=True, null=True)
    gate_pass_authorised_by = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_centre'


class ServiceCustomer(models.Model):
    service_customer_id = models.CharField(primary_key=True, max_length=36)
    service_customer_name = models.TextField(blank=True, null=True)
    service_customer_contact = models.CharField(max_length=250, blank=True, null=True)
    service_customer_email = models.CharField(max_length=250, blank=True, null=True)
    service_customer_visitno = models.IntegerField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    edited_by = models.CharField(max_length=36, blank=True, null=True)
    edited_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_customer'


class ServiceJobCard(models.Model):
    service_job_card_id = models.CharField(primary_key=True, max_length=36)
    service_id = models.CharField(max_length=36, blank=True, null=True)
    job_number = models.CharField(max_length=250, blank=True, null=True)
    service_type = models.CharField(max_length=250, blank=True, null=True)
    item_description = models.CharField(max_length=250, blank=True, null=True)
    item_quantity = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    item_price = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    job_time = models.IntegerField(blank=True, null=True)
    line_total = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    item_notes = models.TextField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    cancelled = models.CharField(max_length=1, blank=True, null=True)
    cancelled_by = models.CharField(max_length=250, blank=True, null=True)
    cancelled_on = models.DateTimeField(blank=True, null=True)
    job_done = models.CharField(max_length=1, blank=True, null=True)
    job_requested = models.CharField(max_length=1, blank=True, null=True)
    local_service = models.CharField(max_length=1, blank=True, null=True)
    discount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    primary_job = models.CharField(max_length=1, blank=True, null=True)
    part_no = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_job_card'


class ServiceJobTool(models.Model):
    service_job_tool_id = models.CharField(primary_key=True, max_length=36)
    service_vehicle_tool_id = models.CharField(max_length=36, blank=True, null=True)
    job_number = models.CharField(max_length=250, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.CharField(max_length=36, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_job_tool'


class ServiceType(models.Model):
    service_type_id = models.CharField(primary_key=True, max_length=36)
    service_code = models.CharField(max_length=10, blank=True, null=True)
    service_name = models.CharField(max_length=250, blank=True, null=True)
    service_charge = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    review_price = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    vattable = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_type'


class ServiceVehicle(models.Model):
    service_vehicle_id = models.CharField(primary_key=True, max_length=36)
    vehicle_reg = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    vin_no = models.CharField(max_length=100, blank=True, null=True)
    engine_no = models.CharField(max_length=100, blank=True, null=True)
    kilometer = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    date_of_registration = models.DateTimeField(blank=True, null=True)
    selling_delear = models.CharField(max_length=250, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_vehicle'


class ServiceVehicleTools(models.Model):
    service_vehicle_tool_id = models.CharField(primary_key=True, max_length=36)
    tool_name = models.CharField(max_length=250, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    tool_code = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_vehicle_tools'


class Sessions(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    user_id = models.PositiveBigIntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    payload = models.TextField()
    last_activity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sessions'


class Shift(models.Model):
    shift_id = models.CharField(primary_key=True, max_length=36)
    shift_day = models.CharField(max_length=1)
    shift_complete = models.CharField(max_length=1)
    sdate = models.DateField()
    shift_description = models.CharField(max_length=20)
    branch_id = models.IntegerField(blank=True, null=True)
    till_id = models.CharField(max_length=36, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shift'


class SmsSetting(models.Model):
    sms_setting_id = models.CharField(primary_key=True, max_length=36)
    sms_setting_message = models.TextField(blank=True, null=True)
    sms_setting_name = models.CharField(max_length=1, blank=True, null=True)
    sms_setting_bal = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sms_setting'


class Staff(models.Model):
    staff_id = models.CharField(primary_key=True, max_length=36)
    staff_id_no = models.CharField(max_length=20)
    staff_code = models.CharField(max_length=10)
    staff_category = models.ForeignKey('StaffCategory', models.DO_NOTHING)
    staff_salary = models.BigIntegerField(blank=True, null=True)
    staff_tel_no = models.TextField()
    staff_nok = models.TextField()
    staff_nhif_no = models.CharField(max_length=25, blank=True, null=True)
    staff_nssf_no = models.CharField(max_length=10, blank=True, null=True)
    staff_sir_name = models.TextField()
    staff_other_names = models.TextField()
    branch_id = models.IntegerField(blank=True, null=True)
    nhif_deduction = models.CharField(max_length=1, blank=True, null=True)
    nssf_deduction = models.CharField(max_length=1, blank=True, null=True)
    staff_salary_bal = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    staff_pinno = models.TextField(blank=True, null=True)
    bank_id = models.IntegerField(blank=True, null=True)
    bank_accno = models.TextField(blank=True, null=True)
    bank_code = models.TextField(blank=True, null=True)
    staffpin = models.TextField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    active = models.CharField(max_length=1, blank=True, null=True)
    nhifamount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    nssfamount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    fprint = models.TextField(blank=True, null=True)
    branch_code = models.CharField(max_length=50, blank=True, null=True)
    branch_name = models.CharField(max_length=50, blank=True, null=True)
    bank_name = models.CharField(max_length=50, blank=True, null=True)
    hascustomeracc = models.CharField(max_length=1, blank=True, null=True)
    customer_id = models.CharField(max_length=36, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'staff'


class StaffCategory(models.Model):
    staff_category_id = models.CharField(primary_key=True, max_length=36)
    staff_category_description = models.CharField(max_length=50)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'staff_category'


class StaffInsuarance(models.Model):
    staffinsuarance_id = models.CharField(primary_key=True, max_length=36)
    staff_id = models.CharField(max_length=36, blank=True, null=True)
    insuarance_id = models.CharField(max_length=36, blank=True, null=True)
    relief_amount = models.IntegerField(blank=True, null=True)
    insuarance_refno = models.TextField(blank=True, null=True)
    active = models.CharField(max_length=1, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    edited_on = models.DateTimeField(blank=True, null=True)
    edited_by = models.CharField(max_length=36, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'staff_insuarance'


class StatusLogs(models.Model):
    status_log_id = models.IntegerField(primary_key=True)
    status_log_start = models.DateTimeField(blank=True, null=True)
    status_log_end = models.DateTimeField(blank=True, null=True)
    start_by = models.IntegerField(blank=True, null=True)
    end_by = models.IntegerField(blank=True, null=True)
    status_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'status_logs'


class StockF(models.Model):
    product_id = models.CharField(primary_key=True, max_length=36)
    product_short_desc = models.TextField(blank=True, null=True)
    product_long_desc = models.TextField(blank=True, null=True)
    uom_code = models.CharField(max_length=3, blank=True, null=True)
    product_quantity = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    product_max_quantity = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    product_min_quantity = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    product_reorder_level = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    product_code = models.CharField(max_length=20, blank=True, null=True)
    product_scancode = models.CharField(max_length=30, blank=True, null=True)
    product_sp = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    product_sp_vat = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    product_bp = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    product_bp_vat = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    batch_tracking = models.CharField(max_length=1, blank=True, null=True)
    active = models.CharField(max_length=1, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    packaging_uom = models.CharField(max_length=3, blank=True, null=True)
    packaging_fixed = models.CharField(max_length=1, blank=True, null=True)
    packaging_ratio = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    packaging_qty = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    fuel_vat = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_f'


class Stocktake(models.Model):
    stk_id = models.CharField(primary_key=True, max_length=36)
    stk_date = models.DateTimeField(blank=True, null=True)
    stk_ref = models.CharField(max_length=50, blank=True, null=True)
    stk_complete = models.CharField(max_length=1, blank=True, null=True)
    stk_cancelled = models.CharField(max_length=1, blank=True, null=True)
    stk_items = models.IntegerField(blank=True, null=True)
    product_id = models.CharField(db_column='Product_id', max_length=36, blank=True, null=True)  # Field name made lowercase.
    product_quantity = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    uom_code = models.CharField(max_length=3, blank=True, null=True)
    location_id = models.CharField(max_length=36, blank=True, null=True)
    curqty = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    pystock = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    packaging = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stocktake'


class Supplier(models.Model):
    supplier_id = models.CharField(primary_key=True, max_length=36)
    supplier_name = models.TextField()
    supplier_pin = models.CharField(db_column='Supplier_pin', max_length=50, blank=True, null=True)  # Field name made lowercase.
    supplier_running_bal = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    supplier_bank_acc = models.CharField(max_length=10, blank=True, null=True)
    supplier_phone_no = models.CharField(max_length=16)
    supplier_address = models.CharField(max_length=50, blank=True, null=True)
    supplier_contact_person = models.CharField(max_length=30, blank=True, null=True)
    supplier_code = models.CharField(max_length=10, blank=True, null=True)
    supplier_total_debit = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    supplier_total_credit = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    active = models.CharField(max_length=1, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'supplier'


class SupplierTrans(models.Model):
    supplier_trans_id = models.CharField(primary_key=True, max_length=36)
    transaction_ref = models.CharField(max_length=250, blank=True, null=True)
    transaction_date = models.DateTimeField(blank=True, null=True)
    transaction_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    transaction_approved = models.CharField(max_length=1, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, models.DO_NOTHING, blank=True, null=True)
    trans_type = models.ForeignKey('TransType', models.DO_NOTHING, blank=True, null=True)
    transaction_payment_type = models.TextField(blank=True, null=True)
    transaction_payment_ref = models.TextField(blank=True, null=True)
    transaction_comment = models.TextField(blank=True, null=True)
    transaction_vat_total = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    transaction_due_date = models.DateTimeField(blank=True, null=True)
    trans_by = models.CharField(max_length=50, blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    running_bal = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    discount = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'supplier_trans'



class SyncTable(models.Model):
    tablename = models.CharField(primary_key=True, max_length=50)
    pkey = models.CharField(max_length=50, blank=True, null=True)
    mfile = models.CharField(max_length=1, blank=True, null=True)
    crossupdate = models.CharField(max_length=1, blank=True, null=True)
    norder = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sync_table'


class SysUser(models.Model):
    user_id = models.CharField(primary_key=True, max_length=36)
    staff_id = models.CharField(max_length=155)
    user_name = models.TextField(db_column='User_name')  # Field name made lowercase.
    user_pass = models.TextField(blank=True, null=True)
    user_pin = models.TextField(blank=True, null=True)
    user_lid = models.IntegerField(blank=True, null=True)
    card_details = models.TextField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    fprint = models.TextField(blank=True, null=True)
    referal_code = models.TextField(blank=True, null=True)
    referal_user = models.TextField(blank=True, null=True)
    referal_count = models.IntegerField(blank=True, null=True)
    paid= models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sys_user'


class SysVat(models.Model):
    vat_id = models.IntegerField(primary_key=True)
    tax_value = models.IntegerField()
    vat_code = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sys_vat'


class Tables(models.Model):
    table_id = models.CharField(primary_key=True, max_length=36)
    table_description = models.CharField(max_length=50, blank=True, null=True)
    table_capacity = models.IntegerField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tables'


class TeamUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    team_id = models.PositiveBigIntegerField()
    user_id = models.PositiveBigIntegerField()
    role = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'team_user'
        unique_together = (('team_id', 'user_id'),)


class Teams(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.PositiveBigIntegerField()
    name = models.CharField(max_length=255)
    personal_team = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teams'


class Till(models.Model):
    till_id = models.CharField(primary_key=True, max_length=36)
    till_no = models.CharField(max_length=36, blank=True, null=True)
    till_printer_port = models.CharField(max_length=10, blank=True, null=True)
    till_receipt_msg1 = models.CharField(max_length=40, blank=True, null=True)
    till_receipt_msg2 = models.CharField(max_length=40, blank=True, null=True)
    locations = models.TextField(blank=True, null=True)
    till_pole_port = models.TextField(blank=True, null=True)
    till_pole_active = models.CharField(max_length=1, blank=True, null=True)
    tillogout = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    confirmrct = models.CharField(max_length=1, blank=True, null=True)
    till_report_port = models.CharField(max_length=50, blank=True, null=True)
    tillchangeqty = models.CharField(max_length=1, blank=True, null=True)
    cashiermac = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'till'


class TransFile(models.Model):
    trans_id = models.CharField(primary_key=True, max_length=36)
    trans_date = models.DateTimeField(blank=True, null=True)
    trans_reference = models.CharField(max_length=250, blank=True, null=True)
    branch_id = models.TextField(blank=True, null=True)
    trans_type = models.ForeignKey('TransType', models.DO_NOTHING, blank=True, null=True)
    uom_code = models.CharField(max_length=3, blank=True, null=True)
    trans_quantity = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    trans_base_quantity = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    batch_no = models.TextField(blank=True, null=True)
    trans_comment = models.TextField(blank=True, null=True)
    product = models.ForeignKey(StockF, models.DO_NOTHING, blank=True, null=True)
    location_product_id = models.CharField(max_length=36, blank=True, null=True)
    complete = models.CharField(max_length=1, blank=True, null=True)
    cancelled = models.CharField(max_length=1, blank=True, null=True)
    supplier_id = models.CharField(max_length=36, blank=True, null=True)
    location_id = models.CharField(max_length=36, blank=True, null=True)
    del_note = models.CharField(max_length=50, blank=True, null=True)
    inv_no = models.CharField(max_length=50, blank=True, null=True)
    lpo_no = models.CharField(max_length=50, blank=True, null=True)
    cost_price = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    running_balance = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    confirmed = models.CharField(max_length=1, blank=True, null=True)
    batch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    track_no = models.CharField(max_length=50, blank=True, null=True)
    packaging_runbal = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    packaging = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    created_by = models.TextField(max_length=36, blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    sprice = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    lpono = models.CharField(max_length=50, blank=True, null=True)
    tran_discount = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    grn_no = models.IntegerField(blank=True, null=True)
    ln = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trans_file'


class TransType(models.Model):
    trans_type_id = models.IntegerField(primary_key=True)
    trans_type_desc = models.CharField(max_length=50, blank=True, null=True)
    trans_type_sign = models.CharField(max_length=1, blank=True, null=True)
    trans_type_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trans_type'


class TripDetails(models.Model):
    trip_details_id = models.CharField(max_length=36)
    trip_id = models.CharField(max_length=36, blank=True, null=True)
    transaction_ref = models.CharField(max_length=225, blank=True, null=True)
    receipt_id = models.CharField(max_length=36, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trip_details'


class Trips(models.Model):
    trip_id = models.CharField(max_length=36)
    route_id = models.CharField(max_length=36, blank=True, null=True)
    trip_date = models.DateTimeField(blank=True, null=True)
    trip_ref = models.CharField(max_length=50, blank=True, null=True)
    trip_customerno = models.IntegerField(blank=True, null=True)
    trip_invoiceno = models.IntegerField(blank=True, null=True)
    trip_done = models.CharField(max_length=1, blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    vehicle_id = models.CharField(max_length=36, blank=True, null=True)
    driver_id = models.CharField(max_length=36, blank=True, null=True)
    driver_name = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trips'


class Tutorial(models.Model):
    title = models.CharField(max_length=70)
    description = models.CharField(max_length=200)
    published = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tutorial'


class Uom(models.Model):
    uom_code = models.CharField( max_length=3)
    uom_description = models.CharField(max_length=25, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    uom_id = models.CharField(primary_key=True,max_length=36)

    class Meta:
        managed = False
        db_table = 'uom'


class UomConversion(models.Model):
    uom_conversion_id = models.CharField(primary_key=True, max_length=36)
    from_uom_code = models.CharField(max_length=3, blank=True, null=True)
    to_uom_code = models.CharField(max_length=3, blank=True, null=True)
    product_id = models.CharField(max_length=36, blank=True, null=True)
    uom_conversion_rate = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    updated = models.CharField(max_length=1, blank=True, null=True)
    wholesale_price = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    retail_price = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    active = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uom_conversion'


class User(models.Model):
    username = models.CharField(max_length=500, blank=True, null=True)
    email = models.CharField(max_length=500, blank=True, null=True)
    password = models.CharField(max_length=1000, blank=True, null=True)
    company_id =models.CharField(max_length=36, blank=True, null=True)
    branch_id = models.IntegerField()
    staff_id = models.CharField(max_length=36, blank=True, null=True)
    bname = models.CharField(max_length=100)
    blocation = models.CharField(max_length=100)
    baddress = models.CharField(max_length=100)
    bphone = models.CharField(max_length=100)
    btill_number = models.CharField(max_length=100)
    b_receipt_footer = models.CharField(max_length=100)
    paid = models.IntegerField()
    verified = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=255)
    two_factor_secret = models.TextField(blank=True, null=True)
    two_factor_recovery_codes = models.TextField(blank=True, null=True)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    current_team_id = models.CharField(max_length=255, blank=True, null=True)
    profile_photo_path = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'

class WeighingDetails(models.Model):
    ticket_no = models.CharField(primary_key=True, max_length=50)
    vehicle_no = models.CharField(max_length=50)
    account = models.CharField(max_length=250)
    field_1 = models.CharField(max_length=50)
    product_name = models.CharField(max_length=250)
    operator_name = models.CharField(max_length=250)
    tare_datetime = models.CharField(max_length=20)
    gross_datetime = models.CharField(max_length=20)
    gross_wt = models.DecimalField(max_digits=12, decimal_places=2)
    tare_wt = models.DecimalField(max_digits=12, decimal_places=2)
    net_wt = models.DecimalField(max_digits=12, decimal_places=2)
    units = models.CharField(max_length=20, blank=True, null=True)
    remarks = models.CharField(max_length=500)
    ticket_date = models.DateTimeField()
    vehicle_indate = models.CharField(max_length=20)
    vehicle_outdate = models.CharField(max_length=20)
    transporter_name = models.CharField(max_length=250)
    intime = models.TimeField()
    outtime = models.TimeField()
    updated = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'weighing_details'

class MpesaPayment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    merchant_request_id = models.CharField(max_length=100)
    checkout_request_id = models.CharField(max_length=100)
    result_code = models.CharField(max_length=10)
    result_desc = models.CharField(max_length=100)
    amount = models.CharField(max_length=36, blank=True, null=True)
    mpesa_receipt_number = models.CharField(max_length=36, blank=True, null=True)
    transaction_date = models.DateTimeField()
    phone_number = models.CharField(max_length=36, blank=True, null=True)
    branch_id = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'mpesa_payment'

class Subscription(models.Model):
    branch_id = models.CharField(max_length=50)
    plan = models.CharField(max_length=50)
    amount = models.IntegerField()
    payment_method = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20)
    class Meta:
        managed = False
        db_table = 'subscription'

class LocationServiceExtra(models.Model):
    extra_id = models.AutoField(primary_key=True)
    service_id = models.CharField(max_length=36, )
    extra_description = models.CharField(max_length=100)
    extra_commission = models.FloatField()
    update_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    branch_id = models.CharField(max_length=36)

    class Meta:
        managed = False
        db_table = 'location_service_extra'

class PosReceiptEtraDetails(models.Model):
    pos_receipt_etra_details_id = models.AutoField(primary_key=True)
    service_id = models.CharField(max_length=36)
    staff_id = models.CharField(max_length=36)
    service_name = models.CharField(max_length=36)
    staff_name = models.CharField(max_length=36)
    branch_id = models.CharField(max_length=36)
    commission_amount = models.FloatField()
    paid = models.CharField(max_length=1)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'pos_receipt_etra_details'

class CommissionTrans(models.Model):
    commission_trans_id = models.AutoField(primary_key=True)
    staff_id = models.CharField(max_length=36) # Field name made lowercase.
    staff_catgory_id = models.CharField(max_length=36)
    amount_paid = models.FloatField()
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'commission_trans'


