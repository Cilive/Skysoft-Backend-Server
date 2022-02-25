from django.db import models
from administrator.models import Branches, Company, Employee


# Create your models here.
class VatMaster(models.Model):
    branches = models.ForeignKey(
        Branches, on_delete=models.DO_NOTHING, null=True)
    # branch=models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)
    vat = models.FloatField()
    company = models.ForeignKey(
        Company, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'vat_master'


class FuelMaster(models.Model):
    # branches = models.ForeignKey(Branches, on_delete=models.DO_NOTHING, null=True)
    name = models.CharField(max_length=30)
    fuel_vat = models.IntegerField()
    rate = models.FloatField(null=True)
    payable_amt = models.FloatField(null=True)
    current_stock = models.FloatField(null=True)
    company = models.ForeignKey(
        Company, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'fuel_master'

    @property
    def get_payable_amt(self):
        try:
            if self.fuel_vat == 0:
                print("inner if condition working")
                payable_amt = self.rate
            elif self.fuel_vat == None:
                payable_amt = self.rate
            else:
                payable_amt = self.rate*self.fuel_vat/100+self.rate
        except Exception as e:
            print(e)
            pass
        return payable_amt

    def __str__(self):
        return str(self.id)
    # used to calcuate fuel payable amount

    def save(self, *args, **kwargs):
        print("========================================= Fuel Master save function working====================================")
        try:
            self.payable_amt = self.get_payable_amt
            super(FuelMaster, self).save(*args, **kwargs)
        except:
            pass


class Owner(models.Model):
    # branch=models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)
    branches = models.ForeignKey(
        Branches, on_delete=models.DO_NOTHING, null=True)
    name = models.CharField(max_length=30)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING,
                                null=True)
    phone = models.CharField(max_length=30,)
    email = models.EmailField(max_length=100,)


class BankAccountMaster(models.Model):
    # date = models.DateField()
    # branch=models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)
    branches = models.ForeignKey(
        Branches, on_delete=models.DO_NOTHING, null=True)
    bank_name = models.CharField(max_length=30)
    acc_holder_name = models.CharField(max_length=30)
    acc_no = models.CharField(max_length=30)
    initial_balance = models.FloatField(null=True)
    balance = models.FloatField(null=True)
    credit_balance = models.FloatField(null=True)
    debit_balance = models.FloatField(null=True)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    company = models.ForeignKey(
        Company, on_delete=models.DO_NOTHING, null=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'bank_account_master'

    def __str__(self):
        return self.bank_name

    @property
    def get_balance(self):
        try:
            if self.initial_balance:
                balance = self.initial_balance
        except Exception as e:
            print(e)
            pass
        return balance

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        print("========================================= BNAK BALANCE FUNCTION working====================================")
        try:
            self.balance = self.get_balance
            super(BankAccountMaster, self).save(*args, **kwargs)
        except:
            pass


class CashMaster(models.Model):
    branches = models.ForeignKey(
        Branches, on_delete=models.DO_NOTHING, null=True)
    company = models.ForeignKey(
        Company, on_delete=models.DO_NOTHING, null=True)
    opening_balance = models.FloatField(null=True)
    balance = models.FloatField(null=True)
    cash_ac_name = models.CharField(max_length=30, null=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True)
    credit_balance = models.FloatField(null=True, default=0)
    debit_balance = models.FloatField(null=True, default=0)

    class Meta:
        db_table = 'cash_master'

    def __str__(self):
        return self.cash_ac_name

    @property
    def get_balance(self):
        try:
            if self.opening_balance:
                balance = self.opening_balance
        except Exception as e:
            print(e)
            pass
        return balance

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        print("========================================= CASH BALANCE FUNCTION working====================================")
        try:
            self.balance = self.get_balance
            super(CashMaster, self).save(*args, **kwargs)
        except:
            pass


class PaymentOut(models.Model):
    # branch=models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)
    branches = models.ForeignKey(
        Branches, on_delete=models.DO_NOTHING, null=True)
    date = models.DateTimeField(auto_now_add=True)
    # supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE,null=True,verbose_name='supplier')
    bank = models.ForeignKey(
        BankAccountMaster, on_delete=models.CASCADE, null=True, verbose_name='bank')
    ref_no = models.CharField(max_length=30)
    paid_amt = models.FloatField()
    # balance_amt = models.FloatField() # auto
    paid_type = models.CharField(max_length=30)
    total_amt = models.FloatField()
    company = models.ForeignKey(
        Company, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'payment_out'

    def __str__(self):
        return str(self.id)


class Expense(models.Model):
    # branch=models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)
    branches = models.ForeignKey(
        Branches, on_delete=models.DO_NOTHING, null=True)
    date = models.DateTimeField(auto_now_add=True)
    exp_type = models.CharField(max_length=30)
    bank = models.ForeignKey(
        BankAccountMaster, on_delete=models.CASCADE, null=True, verbose_name='bank')
    ref_no = models.CharField(max_length=30)
    paid_amt = models.FloatField()
    company = models.ForeignKey(
        Company, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'expense'

    def __str__(self):
        return str(self.id)


class Deposit(models.Model):
    # branch=models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)
    branches = models.ForeignKey(
        Branches, on_delete=models.DO_NOTHING, null=True)
    amount = models.FloatField()
    date = models.DateTimeField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(
        Company, on_delete=models.DO_NOTHING, null=True)
    bank = models.ForeignKey(
        BankAccountMaster, on_delete=models.CASCADE, null=True, verbose_name='bank')

    class Meta:
        db_table = 'deposit'

    def __str__(self):
        return str(self.id)


class Dispence(models.Model):
    # branch=models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)
    branches = models.ForeignKey(
        Branches, on_delete=models.DO_NOTHING, null=True)
    name = models.CharField(max_length=30)
    company = models.ForeignKey(
        Company, on_delete=models.DO_NOTHING, null=True)
    fuel = models.ForeignKey(
        FuelMaster, on_delete=models.CASCADE, null=True, verbose_name='fuel')

    class Meta:
        db_table = 'dispence'

    def __str__(self):
        return str(self.name)


class MeterReading(models.Model):
    # branch=models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)
    branches = models.ForeignKey(
        Branches, on_delete=models.DO_NOTHING, null=True)
    date = models.DateTimeField()
    start_reading = models.FloatField()
    end_reading = models.FloatField()
    # previous_reading = models.FloatField()
    payable_amt = models.FloatField()
    fuel = models.ForeignKey(
        FuelMaster, on_delete=models.CASCADE, null=True, verbose_name='fuel')
    fuel_stock = models.FloatField(null=True, default=0)
    # liter = models.FloatField() # auto
    # stock = models.FloatField() # auto
    dispence = models.ForeignKey(Dispence, on_delete=models.CASCADE,
                                 null=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING,
                                null=True, related_name='meter_reading_company')
    employee = models.ForeignKey(
        Employee, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'meter_reading'

    def __str__(self):
        return str(self.date)


class Contact(models.Model):
    USER_CHOICES = (
        ("1", "customer"),
        ("2", "supplier"),
    )
    en_name = models.CharField(max_length=30)
    ar_name = models.CharField(max_length=30)
    en_place = models.CharField(max_length=30)
    ar_place = models.CharField(max_length=30)
    en_district = models.CharField(max_length=30)
    ar_district = models.CharField(max_length=30)
    vat_no = models.CharField(max_length=15)
    lan_no = models.CharField(max_length=15)
    mobile_no = models.CharField(max_length=15, unique=True)
    company = models.ForeignKey(
        Company, on_delete=models.DO_NOTHING, null=True)
    branches = models.ForeignKey(
        Branches, on_delete=models.DO_NOTHING, null=True)
    type = models.CharField(max_length=15, choices=USER_CHOICES, default='1')
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'contact'

    def __str__(self):
        return self.en_name


class DailySession(models.Model):
    branches = models.ForeignKey(
        Branches, on_delete=models.DO_NOTHING, null=True)
    opening_balance_bank = models.FloatField(null=True)
    cash_opening_balance = models.FloatField(null=True)
    closing_balance_bank = models.FloatField(null=True)
    closing_balance_cash = models.FloatField(null=True)
    total_transactions = models.FloatField(null=True)
    total_sales = models.FloatField(null=True)
    total_purchase = models.FloatField(null=True)
    total_expense = models.FloatField(null=True)
    total_cash_sales = models.FloatField(null=True)
    total_cash_purchase = models.FloatField(null=True)
    total_bank_purchase = models.FloatField(null=True)
    total_bank_sales = models.FloatField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(
        Company, on_delete=models.DO_NOTHING, null=True)
    bank = models.ForeignKey(
        BankAccountMaster, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'daily_session_master'

    def __str__(self):
        return str(self.id)


class Invoice(models.Model):
    PAYMENT_TYPE = (
        ("1", "CASH"),
        ("2", "BANK"),
        ("3", "CREDIT"),
    )
    TYPE = (
        ("1", "in_invoice"),
        ("2", "out_invoice"),
        ("3", "expense"),
    )

    invoice_no = models.BigIntegerField(null=True, blank=True, default=None)
    session = models.ForeignKey(
        DailySession, on_delete=models.CASCADE, null=True)
    branches = models.ForeignKey(
        Branches, on_delete=models.DO_NOTHING, null=True)
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, null=True, verbose_name='contact', blank=True)
    emp = models.ForeignKey(Employee, on_delete=models.DO_NOTHING,
                            null=True, verbose_name='employee', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    fuel = models.ForeignKey(
        FuelMaster, on_delete=models.CASCADE, null=True, verbose_name='fuel')
    qty = models.FloatField()
    gross_amt = models.FloatField(null=True, blank=True)  # auto
    payment_type = models.CharField(
        max_length=15, choices=PAYMENT_TYPE, default='1')
    type = models.CharField(max_length=15, choices=TYPE, default='1')
    total_amt = models.FloatField(null=True, blank=True)  # auto
    credit_amount = models.FloatField(null=True, blank=True)
    account_number = models.CharField(max_length=15, null=True, blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.DO_NOTHING, null=True)
    vat = models.ForeignKey(VatMaster, on_delete=models.CASCADE, null=True)
    bank = models.ForeignKey(
        BankAccountMaster, on_delete=models.CASCADE, null=True)
    cash = models.ForeignKey(CashMaster, on_delete=models.CASCADE, null=True)
    vat_percenatge = models.FloatField(null=True, blank=True)
    vat_amount = models.FloatField(null=True, blank=True)
    paid_amt = models.FloatField(null=True, blank=True, default=0)
    balance_amt = models.FloatField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    exp_type = models.CharField(max_length=30, null=True, blank=True)
    ref_no = models.CharField(max_length=30, null=True, blank=True)
    fuelvat_percentage = models.FloatField(null=True, blank=True, default=0)
    base_64_encoded = models.TextField(null=True, blank=True, default=0)

    class Meta:
        db_table = 'invoice'

    # @property
    # def get_gross_amt(self):
    #     gross_amt = self.qty*self.fuel.payable_amt
    #     return gross_amt

    # @property
    # def get_vat_percentage(self):
    #     if self.vat:
    #         vat_percentage = self.vat.vat
    #     else:
    #         vat_percentage=0
    #     return vat_percentage
    @property
    def get_account_number(self):
        if self.bank:
            account_number = self.bank.acc_no
        else:
            account_number = None

        return account_number

    @property
    def get_fuel_vat_percentage(self):
        if self.fuel:
            fuel_vat_percentage = self.fuel.fuel_vat
        else:
            fuel_vat_percentage = 0
        return fuel_vat_percentage

    # @property
    # def get_total_amount(self):
    #     common_vat=self.gross_amt*self.vat_percenatge/100
    #     total=self.gross_amt+common_vat
    #     return total

    # @property
    # def get_vat_amount(self):
    #     try:
    #         vat_amount=self.gross_amt*self.vat_percenatge/100
    #         return vat_amount
    #     except Exception as e:
    #         print(e)
    #         return 0

    @property
    def get_balance_amt(self):
        # total_amt=
        try:
            balance = 0
            print("total amount", self.total_amt)
            print("type ", self.type)
            print("type ", type(self.type))
            if int(self.type) == 1:
                print("Its a purchase")
                # if self.paid_amt==0:
                #     balance=0
                try:

                    if self.paid_amt == 0:
                        # print(" inner if self paid amount",self.paid_amt)
                        balance: float = float(
                            self.total_amt)-float(self.paid_amt)
                    elif float(self.paid_amt) == float(self.total_amt):
                        print(" inner if self paid amount", self.paid_amt)
                        try:
                            balance: float = 0
                        except Exception as e:
                            print(e)

                    else:
                        balance: float = float(
                            self.total_amt)-float(self.paid_amt)
                except Exception as e:
                    print(e)
                    # return balance
            if int(self.type) == 2:
                if self.paid_amt == self.total_amt:
                    balance = 0
                else:
                    balance = self.total_amt-self.paid_amt
        except Exception as e:
            print(e)
            pass

        return balance

    def save(self, *args, **kwargs):
        print("=========================================save function working====================================", self.type)
        try:
            # if int(self.type)==3:
            #     print("inner save condition")
            #     self.account_number = self.get_account_number
            #     super(Invoice, self).save(*args, **kwargs)
            # else:
            # self.gross_amt = self.get_gross_amt
            # self.vat_percenatge = self.get_vat_percentage
            self.fuelvat_percentage = self.get_fuel_vat_percentage
            # self.total_amt = self.get_total_amount
            # self.vat_amount = self.get_vat_amount
            self.account_number = self.get_account_number
            self.balance_amt = self.get_balance_amt
            super(Invoice, self).save(*args, **kwargs)
        except Exception as e:
            print("error in save function", e)
            pass

    def __str__(self):
        return str(self.invoice_no)


class FuelStock(models.Model):
    Fuel = models.ForeignKey(FuelMaster, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(
        Company, on_delete=models.DO_NOTHING, null=True)
    branches = models.ForeignKey(
        Branches, on_delete=models.DO_NOTHING, null=True)
    qty = models.FloatField(null=True)

    class Meta:
        db_table = 'fuel_quantity'

    def __str__(self):
        return str(self.Fuel)


class AccountLedger(models.Model):
    branches = models.ForeignKey(
        Branches, on_delete=models.DO_NOTHING, null=True)
    session = models.ForeignKey(
        DailySession, on_delete=models.CASCADE, null=True)
    balance = models.FloatField(null=True)
    debit_balance = models.FloatField(null=True)
    credit_balance = models.FloatField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(
        Company, on_delete=models.DO_NOTHING, null=True)
    bank = models.ForeignKey(
        BankAccountMaster, on_delete=models.CASCADE, null=True)
    cash = models.ForeignKey(CashMaster, on_delete=models.CASCADE, null=True)
    total_transactions = models.FloatField(null=True)
    total_sales = models.FloatField(null=True)
    total_purchase = models.FloatField(null=True)
    total_expense = models.FloatField(null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Daily_Account_Ledger'

    def __str__(self):
        return str(self.id)
