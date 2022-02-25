from datetime import datetime
from administrator.models import (Branches, BranchManager, Company, Employee,
                                  User)
from administrator.serielizer import (BranchesSerializer, CompanySerializer,
                                      UserSerielizer)
from company.models import (AccountLedger, BankAccountMaster, CashMaster,
                            Contact, DailySession, Deposit, Dispence,
                            FuelMaster, FuelStock, Invoice, MeterReading,
                            Owner, VatMaster)
from django.db.models import Q
from django.db.models.aggregates import Sum
from fatoora import Fatoora
from rest_framework import serializers

from .utils import Util


class CustomerCraeteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

    def save(self):
        manger = BranchManager.objects.get(user=self.context['request'].user)
        print("company=", manger.branches_id)
        company = Company.objects.get(id=manger.company_id)
        print("company=", company)

        conatct = Contact(
            **self.validated_data,
            company=Company.objects.get(id=manger.company_id),
            branches=Branches.objects.get(id=manger.branches_id)
        )
        conatct.save()
        return conatct


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class SupplierCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

    def save(self):
        manger = BranchManager.objects.get(user=self.context['request'].user)
        print("company=", manger.branches_id)
        company = Company.objects.get(id=manger.company_id)
        print("company=", company)

        conatct = Contact(
            **self.validated_data,
            company=Company.objects.get(id=manger.company_id),
            branches=Branches.objects.get(id=manger.branches_id)
        )
        conatct.save()
        return conatct


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class CustomerListSerielizer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'en_name']


class BankAccountListSerielizer(serializers.ModelSerializer):
    class Meta:
        model = BankAccountMaster
        fields = ['id', 'acc_holder_name', 'is_default', 'acc_no', 'balance']


class SaleReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = ['date', 'qty', 'payment_type', 'gross_amt',
                  'vat_amount', 'total_amt', 'vat_percenatge', 'invoice_no']

    def to_representation(self, instance):
        # print("data from view ",self.context['dateto'])
        self.context['request'].user
        response = super().to_representation(instance)
        company_data = CompanySerializer(instance.company).data
        customer_data = CustomerSerializer(instance.contact).data
        fuel = FuelSerializer(instance.fuel).data
        print("Fuel in isntance ============================>", fuel)
        branch = BranchesSerializer(instance.branches).data
        if instance.payment_type == '1':
            response.pop('payment_type')
            response['payment_type'] = "Cash"
        elif instance.payment_type == '2':
            response.pop('payment_type')
            response['payment_type'] = "Online"
        try:
            response['username'] = company_data['user']['username']
            response['description'] = fuel['name']
            response['price'] = fuel['payable_amt']
            response['customer'] = customer_data['en_name']
            response['um'] = "Ltr"
            response['branch'] = branch['en_name']

        except TypeError:
            pass

        return response


class ExpenseReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = ['date', 'payment_type', 'gross_amt',
                  'total_amt', 'invoice_no', 'exp_type', 'ref_no']

    def to_representation(self, instance):
        # print("data from view ",self.context['dateto'])
        self.context['request'].user
        response = super().to_representation(instance)
        company_data = CompanySerializer(instance.company).data
        customer_data = CustomerSerializer(instance.contact).data
        branch = BranchesSerializer(instance.branches).data
        if instance.payment_type == '1':
            response.pop('payment_type')
            response['payment_type'] = "Cash"
        elif instance.payment_type == '2':
            response.pop('payment_type')
            response['payment_type'] = "Online"
        try:
            response['username'] = company_data['user']['username']
            response['customer'] = customer_data['en_name']
            response['branch'] = branch['en_name']

        except TypeError:
            pass

        return response


class InvoiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

    def save(self):
        print("bank account serielizer running", self.context['data']['type'])
        print("data in serielizer running", self.context['data'])
        # print("Branches in  serielizer running",self.context['data']['branches'])
        print("session in  serielizer running",
              self.context['data']['session_id'])
        manger = BranchManager.objects.get(user=self.context['request'].user)
        company = Company.objects.get(id=manger.company_id)
        company_name = company.en_name
        company_vat = company.vat_no
        print("company name", company_name)
        tag1_company_name = str(company_name)
        tag_2_company_vat = str(company_vat)
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tag3_date_time = str(current_datetime)
        invoice_total = str(self.validated_data['total_amt'])
        vat_total = str(self.validated_data['vat_amount'])
        fatoora_obj = Fatoora(
            seller_name=tag1_company_name,
            tax_number=int(tag_2_company_vat),  # or "1234567891"
            # timestamp or datetime object, or string ISO 8601 Zulu format
            invoice_date=tag3_date_time,
            total_amount=invoice_total,  # or 100.0, 100.00, "100.0", "100.00"
            tax_amount=vat_total,  # or 15.0, 15.00, "15.0", "15.00"
        )
        print(fatoora_obj.base64)

        type = self.context['data']['type']
        # branch=self.context['data']['branches']
        session = self.context['data']['session_id']
        print("type=", type)
        # last_invoice = Invoice.objects.filter(Q(type=type) ).order_by('id').last()
        last_invoice = Invoice.objects.filter(type=2).order_by('id').last()
        if not last_invoice:
            new_invoice_int = 1
        else:
            invoice_no = last_invoice.invoice_no
            invoice_int = int(invoice_no)
            new_invoice_int = invoice_int + 1
        print(last_invoice)
        print("New invocie number", new_invoice_int)
        print(self.validated_data)
        try:
            vat = VatMaster.objects.get(company=manger.company_id)
        except VatMaster.DoesNotExist:
            vat = None
        try:
            print("checking is there a bank account")
            try:
                ac_id = self.context['data']['bank_ac_id']
                if ac_id:
                    bank = BankAccountMaster.objects.get(
                        company=manger.company_id, branches=manger.branches_id, id=ac_id)
                    print("bank object", bank)
                else:
                    bank = None
            except:
                bank = None
        except BankAccountMaster.DoesNotExist:
            bank = None
        try:
            print("checking is there a cash account")
            try:
                cash = CashMaster.objects.get(
                    company=manger.company_id, branches=manger.branches_id)
                print("cash object", cash)
            except:
                cash = None
        except CashMaster.DoesNotExist:
            cash = None
        invoice = Invoice(
            **self.validated_data,
            invoice_no=new_invoice_int,
            company=Company.objects.get(id=manger.company_id),
            branches=Branches.objects.get(id=manger.branches_id),
            bank=bank,
            cash=cash,
            vat=vat,
            session=DailySession.objects.get(id=session)
        )
        invoice.save()
        print("===============invoice created succesfully==========", invoice.id)
        self.instance = invoice
        return self.instance


class InvoiceListSerielizer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'date', 'invoice_no',
                  'contact', 'total_amt', 'balance_amt']

    def to_representation(self, instance):
        # print("data from view ",self.context['dateto'])
        response = super().to_representation(instance)
        customer = CustomerSerializer(instance.contact).data
        try:
            # branch=BranchesSerializer(instance.branches).data
            if instance.contact:
                response.pop('contact')
                response['customer_name'] = customer['en_name']
        except TypeError:
            pass

        return response


class InvoiceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['date', 'qty', 'payment_type', 'fuel',
                  'paid_amt', 'balance_amt', 'total_amt']


class VatRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VatMaster
        fields = '__all__'

    def save(self):
        manger = BranchManager.objects.get(user=self.context['request'].user)
        # print(type(self.validated_data['vat']))
        vat = VatMaster(
            **self.validated_data,
            company=Company.objects.get(id=manger.company_id),
            branches=Branches.objects.get(id=manger.branches_id),

        )
        vat.save()
        return vat


class VatSerializer(serializers.ModelSerializer):
    class Meta:
        model = VatMaster
        fields = '__all__'


# class FuelRegistrationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FuelMaster
#         exclude = ['payable_amt']

#     def save(self):
#         manger=BranchManager.objects.get(user=self.context['request'].user)
#         print(self.validated_data)

#         fuel = FuelMaster(
#             name = self.validated_data['name'],
#             fuel_vat = self.validated_data['fuel_vat'],
#             company =Company.objects.get(id=manger.company_id),
#             branches = Branches.objects.get(id=manger.branches_id),
#             rate=self.validated_data['rate'],
#             current_stock=self.validated_data['current_stock'],
#         )
#         fuel.save()
#         self.instance = fuel
#         return self.instance

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['company'] = CompanySerializer(instance.bank).data
    #     return response

class FuelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelMaster
        fields = ('name', 'fuel_vat', 'id', 'rate',
                  'current_stock', 'payable_amt')


class FuelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelMaster
        fields = ['name', 'fuel_vat', 'id', 'rate', 'payable_amt']


class BankCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccountMaster
        fields = '__all__'

    def save(self):
        manger = BranchManager.objects.get(user=self.context['request'].user)
        # if BankAccountMaster.objects.filter(branches=manger.branches_id).exists():
        #     raise serializers.ValidationError({'error':'Already registered an account with this branch'},)

        bank = BankAccountMaster(
            **self.validated_data,
            company=Company.objects.get(id=manger.company_id),
            branches=Branches.objects.get(id=manger.branches_id),
        )
        bank.save()
        return bank

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['company'] = CompanySerializer(instance.bank).data
    #     return response


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccountMaster
        fields = '__all__'


class OwnerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'

    def save(self):
        manger = BranchManager.objects.get(user=self.context['request'].user)
        if Owner.objects.filter(phone=self.validated_data['phone']).exists():
            raise serializers.ValidationError(
                {'error': 'This phone number is already been used'})

        if Owner.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError(
                {'error': 'This email is already exist'})

        owner = Owner(
            **self.validated_data,
            company=Company.objects.get(id=manger.company_id),
            branches=Branches.objects.get(id=manger.branches_id),
        )
        owner.save()
        return owner


class OwnerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'


class DepositCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deposit
        fields = '__all__'

    def save(self):
        manger = BranchManager.objects.get(user=self.context['request'].user)

        ac_id = self.context['data']['bank_ac_id']
        branches = manger.branches_id
        try:
            print("checking is there a bank account")
            try:
                if ac_id:
                    bank = BankAccountMaster.objects.get(
                        company=manger.company_id, branches=branches, id=ac_id)
                    print("bank object", bank)
                else:
                    bank = None
            except:
                bank = None
        except BankAccountMaster.DoesNotExist:
            bank = None
        deposit = Deposit(
            amount=self.validated_data['amount'],
            date=self.validated_data['date'],
            owner=self.validated_data['owner'],
            branches=Branches.objects.get(id=manger.branches_id),
            company=Company.objects.get(id=manger.company_id),
            bank=bank,
        )
        deposit.save()
        print("deposit compnay=", deposit.company.id)
        print("deposit amount=", deposit.amount)
        print("deposit amount=", deposit.branches)

        bank_account = BankAccountMaster.objects.get(
            company=deposit.company, branches=deposit.branches, id=ac_id)
        print("bank account affected", bank_account.balance)
        new_balance = bank_account.balance+deposit.amount
        print("new balance ", new_balance)
        BankAccountMaster.objects.filter(
            company=deposit.company, branches=deposit.branches, id=ac_id).update(balance=new_balance)

        return deposit

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['company'] = CompanySerializer(instance.bank).data
    #     return response


class DepositSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deposit
        fields = '__all__'


class DispenceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispence
        fields = '__all__'

    def save(self):
        manger = BranchManager.objects.get(user=self.context['request'].user)

        dispence = Dispence(
            **self.validated_data,
            company=Company.objects.get(id=manger.company_id),
            branches=Branches.objects.get(id=manger.branches_id),
        )
        dispence.save()
        self.instance = dispence
        return self.instance


class DispenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispence
        fields = '__all__'


class FirstSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailySession
        fields = '__all__'

    def save(self):
        # print("serielizer running")
        # print("serielizer running",)
        manger = BranchManager.objects.get(user=self.context['request'].user)

        branch_info = self.context['data']
        # print("serielizer bank balance",branch_info.balance)
        # print("serielizer cash balance",branch_info.opening_balance)
        # print("serielizer bank balance",branch_info.initial_balance)
        cash_opening_balance = branch_info.opening_balance
        bank_account_opening_balance = BankAccountMaster.objects.get(
            branches=manger.branches_id, is_default=True).initial_balance
        session = DailySession(
            branches=Branches.objects.get(id=manger.branches_id),
            bank=BankAccountMaster.objects.get(
                branches=manger.branches_id, is_default=True),
            opening_balance_bank=bank_account_opening_balance,
            cash_opening_balance=cash_opening_balance,
            company=Company.objects.get(id=manger.company_id)
        )
        session.save()
        self.instance = session
        return self.instance


class SessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailySession
        fields = '__all__'

    def save(self):
        manger = BranchManager.objects.get(user=self.context['request'].user)

        print("session create serielizer running")
        previous_session = self.context['data']
        print("prevoious day balance", previous_session.closing_balance_cash)
        # print("serielizer cash balance",branch_info.opening_balance)
        # print("serielizer bank balance",branch_info.initial_balance)
        cash_opening_balance = previous_session.closing_balance_cash
        bank_account_opening_balance = previous_session.closing_balance_bank
        session = DailySession(
            branches=Branches.objects.get(id=manger.branches_id),
            bank=BankAccountMaster.objects.get(
                branches=manger.branches_id, is_default=True),
            opening_balance_bank=bank_account_opening_balance,
            company=Company.objects.get(id=manger.company_id),
            cash_opening_balance=cash_opening_balance
        )
        session.save()
        self.instance = session
        return self.instance


class CashMasterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashMaster
        fields = '__all__'

    def save(self):
        manger = BranchManager.objects.get(user=self.context['request'].user)
        # maybe ther will be owner for a branch we can speciy it here
        # the branch will be detected from branch users details

        session = CashMaster(
            branches=Branches.objects.get(id=manger.branches_id),
            opening_balance=self.validated_data['opening_balance'],
            balance=self.validated_data['balance'],
            company=Company.objects.get(id=manger.company_id)

        )
        session.save()
        self.instance = session
        return self.instance


class SessionCloseSerielizer(serializers.ModelSerializer):
    class Meta:
        model = DailySession
        fields = '__all__'

    def save(self):
        # print("session",self)s
        print("session", self.context['data'])
        data = self.context['data']
        session = data[0]
        manger = BranchManager.objects.get(user=self.context['request'].user)

        total_transactions = Invoice.objects.filter(
            session=session, branches=manger.branches_id).aggregate(Sum('total_amt'))

        if total_transactions['total_amt__sum'] is None:
            total_transactions = 0
        else:
            total_transactions = total_transactions['total_amt__sum']
        total_sale_by_cash = Invoice.objects.filter(
            session=session, payment_type=1, type=2, branches=manger.branches_id).aggregate(Sum('total_amt'))
        if total_sale_by_cash['total_amt__sum'] is None:
            total_sale_by_cash = 0
        else:
            total_sale_by_cash = total_sale_by_cash['total_amt__sum']
        total_purchase_by_cash = Invoice.objects.filter(
            session=session, payment_type=1, type=1, branches=manger.branches_id).aggregate(Sum('total_amt'))
        if total_purchase_by_cash['total_amt__sum'] is None:
            total_purchase_by_cash = 0
        else:
            total_purchase_by_cash = total_purchase_by_cash['total_amt__sum']
        total_expense_by_cash = Invoice.objects.filter(
            session=session, payment_type=1, type=3, branches=manger.branches_id).aggregate(Sum('total_amt'))
        if total_expense_by_cash['total_amt__sum'] is None:
            total_expense_by_cash = 0
        else:
            total_expense_by_cash = total_expense_by_cash['total_amt__sum']
        total_sale_by_bank = Invoice.objects.filter(
            session=session, payment_type=2, type=2, branches=manger.branches_id).aggregate(Sum('total_amt'))
        if total_sale_by_bank['total_amt__sum'] is None:
            total_sale_by_bank = 0
        else:
            total_sale_by_bank = total_sale_by_bank['total_amt__sum']
        total_purchase_by_bank = Invoice.objects.filter(
            session=session, payment_type=2, type=1, branches=manger.branches_id).aggregate(Sum('total_amt'))
        if total_purchase_by_bank['total_amt__sum'] is None:
            total_purchase_by_bank = 0
        else:
            total_purchase_by_bank = total_purchase_by_bank['total_amt__sum']
        total_expense_by_bank = Invoice.objects.filter(
            session=session, payment_type=2, type=3, branches=manger.branches_id).aggregate(Sum('total_amt'))
        if total_expense_by_bank['total_amt__sum'] is None:
            total_expense_by_bank = 0

        else:
            print("sereializer woring else")
            total_expense_by_bank = total_expense_by_bank['total_amt__sum']
        total_sale = Invoice.objects.filter(
            session=session, type=2, branches=manger.branches_id).aggregate(Sum('total_amt'))
        if total_sale['total_amt__sum'] is None:
            total_sale = 0
        else:
            total_sale = total_sale['total_amt__sum']
        total_purchase = Invoice.objects.filter(
            session=session, type=1, branches=manger.branches_id).aggregate(Sum('total_amt'))
        if total_purchase['total_amt__sum'] is None:
            total_purchase = 0
        else:
            total_purchase = total_purchase['total_amt__sum']
        total_expense = Invoice.objects.filter(
            session=session, type=3, branches=manger.branches_id).aggregate(Sum('total_amt'))
        if total_expense['total_amt__sum'] is None:
            total_expense = 0
        else:
            total_expense = total_expense['total_amt__sum']
        print("total invoice sum", total_transactions)
        print("total cash sales", total_sale_by_cash)
        print("total cash Purchase", total_purchase_by_cash)
        print("total cash expense", total_expense_by_cash)
        print("total bank sales", total_sale_by_bank)
        print("total bank Purchase", total_purchase_by_bank)
        print("total bank expense", total_expense_by_bank)

        cashmaster = CashMaster.objects.filter(branches=session.branches)
        print("cashmaster", cashmaster[0])
        cash_master = cashmaster[0].balance
        print("current blance in cash for the branch", cash_master)
        bankmaster = BankAccountMaster.objects.filter(
            branches=session.branches)
        print("cashmaster", bankmaster[0])
        bank_master_balance = bankmaster[0].balance
        print("current blance in bank for the branch", bank_master_balance)
        try:
            session_update = DailySession.objects.filter(pk=session.id).update(closing_balance_cash=cash_master,
                                                                               closing_balance_bank=bank_master_balance,
                                                                               total_transactions=total_transactions,
                                                                               total_sales=total_sale,
                                                                               total_purchase=total_purchase,
                                                                               total_expense=total_expense,
                                                                               total_cash_sales=total_sale_by_cash,
                                                                               total_cash_purchase=total_purchase_by_cash,
                                                                               total_bank_purchase=total_purchase_by_bank,
                                                                               total_bank_sales=total_sale_by_bank,
                                                                               company=Company.objects.get(
                                                                                   id=manger.company_id),
                                                                               status=True
                                                                               )
        except Exception as e:
            print("error in session close", e)

        print("session update", session_update)
        if session_update == 1:
            cash_accounts = Invoice.objects.values('cash_id').filter(
                session=session.id, cash__isnull=False).distinct()
            print("after session update code=======================>", cash_accounts)
            if not cash_accounts:
                print("no cash accounts found")
                pass
            else:
                cash_ac_id = cash_accounts[0]['cash_id']
                print('session updated suscessfully')
                total_sale_cash = Invoice.objects.filter(
                    session=session.id, payment_type=1, type=2, cash=cash_ac_id, branches=manger.branches_id).aggregate(Sum('total_amt'))
                print(
                    "repsonse from total sale cash===========================>", total_sale_cash)
                if total_sale_cash['total_amt__sum'] is None:
                    print(
                        "================================Value is None ====================================>", total_sale_by_cash)
                    total_sale_by_cash = 0
                else:
                    total_sale_by_cash = total_sale_cash['total_amt__sum']
                    print(
                        "================================Value is NOT NONE ====================================>", total_sale_by_cash)
                total_purchase_cash = Invoice.objects.filter(
                    session=session.id, payment_type=1, type=1, cash=cash_ac_id, branches=manger.branches_id).aggregate(Sum('total_amt'))
                if total_purchase_cash['total_amt__sum'] is None:
                    total_purchase_by_cash = 0
                else:
                    total_purchase_by_cash = total_purchase_cash['total_amt__sum']
                total_expense_cash = Invoice.objects.filter(
                    session=session.id, payment_type=1, type=3, cash=cash_ac_id, branches=manger.branches_id).aggregate(Sum('total_amt'))
                if total_expense_cash['total_amt__sum'] is None:
                    total_expense_by_cash = 0
                else:
                    total_expense_by_cash = total_expense_cash['total_amt__sum']
                total_transactions_by_cash = Invoice.objects.filter(
                    session=session.id, cash=cash_ac_id, payment_type=1, branches=manger.branches_id).aggregate(Sum('total_amt'))
                if total_transactions_by_cash['total_amt__sum'] is None:
                    total_transactions = 0
                else:
                    total_transactions = total_transactions_by_cash['total_amt__sum']
                total_credit = Invoice.objects.filter(
                    session=session.id, cash=cash_ac_id, payment_type=1, type=1, branches=manger.branches_id).aggregate(Sum('balance_amt'))
                if total_credit['balance_amt__sum'] is None:
                    total_credit_by_cash = 0
                else:
                    total_credit_by_cash = total_credit['balance_amt__sum']
                total_debit = Invoice.objects.filter(
                    session=session.id, cash=cash_ac_id, payment_type=1, type=2, branches=manger.branches_id).aggregate(Sum('balance_amt'))
                if total_debit['balance_amt__sum'] is None:
                    total_debitt_by_cash = 0
                else:
                    total_debitt_by_cash = total_debit['balance_amt__sum']
                # cash ledger creation
                try:
                    ledger = AccountLedger(
                        branches=cashmaster[0].branches,
                        session=DailySession.objects.get(id=session.id),
                        debit_balance=total_credit_by_cash,
                        credit_balance=total_debitt_by_cash,
                        balance=cashmaster[0].balance,
                        company=cashmaster[0].company,
                        cash=cashmaster[0],
                        total_transactions=total_transactions,
                        total_sales=total_sale_by_cash,
                        total_purchase=total_purchase_by_cash,
                        total_expense=total_expense_by_cash,

                    )
                    ledger.save()
                    print("cash ledger created", ledger)
                except Exception as e:
                    print(e)

            accounts = Invoice.objects.filter(
                session=session).values('bank_id').distinct()
            print('affected bank accounts', accounts)
            if not accounts:
                print("No accounts affected")
            else:
                print('affected bank accounts', accounts)
                for account in accounts:
                    if account is None:
                        print(account['bank_id'])
                        bank_account_id = account['bank_id']
                        bank = BankAccountMaster.objects.get(
                            id=bank_account_id)
                        print("bank", bank)
                        bank = BankAccountMaster.objects.get(
                            id=bank_account_id)
                        total_sale_account = Invoice.objects.filter(
                            session=session.id, payment_type=2, type=2, bank=bank_account_id, branches=manger.branches_id).aggregate(Sum('total_amt'))
                        if total_sale_account['total_amt__sum'] is None:
                            total_sale_by_account = 0
                        else:
                            total_sale_by_account = total_sale_account['total_amt__sum']
                        total_purchase_account = Invoice.objects.filter(
                            session=session.id, payment_type=2, type=1, bank=bank_account_id, branches=manger.branches_id).aggregate(Sum('total_amt'))
                        if total_purchase_account['total_amt__sum'] is None:
                            total_purchase_by_account = 0
                        else:
                            total_purchase_by_account = total_purchase_account['total_amt__sum']
                        total_expense_account = Invoice.objects.filter(
                            session=session.id, payment_type=2, type=3, bank=bank_account_id, branches=manger.branches_id).aggregate(Sum('total_amt'))
                        if total_expense_account['total_amt__sum'] is None:
                            total_expense_by_account = 0
                        else:
                            total_expense_by_account = total_expense_account['total_amt__sum']
                        total_transactions_by_account = Invoice.objects.filter(
                            session=session.id, bank=bank_account_id, payment_type=2, branches=manger.branches_id).aggregate(Sum('total_amt'))
                        if total_transactions_by_account['total_amt__sum'] is None:
                            total_transactions = 0
                        else:
                            total_transactions = total_transactions_by_account['total_amt__sum']
                        total_credit = Invoice.objects.filter(
                            session=session.id, bank=bank_account_id, payment_type=2, type=1, branches=manger.branches_id).aggregate(Sum('balance_amt'))
                        if total_credit['balance_amt__sum'] is None:
                            total_credit_by_bank = 0
                        else:
                            total_credit_by_bank = total_credit['balance_amt__sum']
                        total_debit = Invoice.objects.filter(
                            session=session.id, bank=bank_account_id, payment_type=2, type=2, branches=manger.branches_id).aggregate(Sum('balance_amt'))
                        if total_debit['balance_amt__sum'] is None:
                            total_debitt_by_bank = 0
                        else:
                            total_debitt_by_bank = total_debit['balance_amt__sum']
                        try:
                            ledger = AccountLedger(
                                branches=bank.branches,
                                session=DailySession.objects.get(
                                    id=session.id),
                                debit_balance=total_debitt_by_bank,
                                credit_balance=total_credit_by_bank,
                                balance=bank.balance,
                                company=bank.company,
                                bank=bank,
                                total_transactions=total_transactions,
                                total_sales=total_sale_by_account,
                                total_purchase=total_purchase_by_account,
                                total_expense=total_expense_by_account,
                            )
                            ledger.save()
                            print("bank ledger created", ledger)
                        except Exception as e:
                            print(e)
                    else:
                        pass
            session_update = DailySession.objects.filter(
                pk=session.id).update(status=1)
        self.instance = session_update
        return self.instance


class SessionCloseResultSerielizer(serializers.ModelSerializer):
    class Meta:
        model = DailySession
        fields = '__all__'


class ReciptCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

    def save(self):
        print("Recipt create serielizer running", self.context['data']['type'])
        print("session in  serielizer running",
              self.context['data']['session_id'])
        manger = BranchManager.objects.get(user=self.context['request'].user)
        type = self.context['data']['type']
        branch = Branches.objects.get(id=manger.branches_id)
        ac_id = BankAccountMaster.objects.get(
            branches=manger.branches_id, is_default=True)
        session = self.context['data']['session_id']
        print("type=", type)
        last_invoice = Invoice.objects.filter(type=1).order_by('id').last()
        # print("last invoice",last_invoice.invoice_no)
        if not last_invoice:
            new_recipt_int = 1
        else:
            invoice_no = last_invoice.invoice_no
            invoice_int = int(invoice_no)
            new_recipt_int = invoice_int + 1
            print(last_invoice)
            print("New invocie number", new_recipt_int)
            print(self.validated_data)

        company = Company.objects.get(id=manger.company_id)
        try:
            vat = VatMaster.objects.get(company=company)
        except VatMaster.DoesNotExist:
            vat = None
        try:
            print("checking is there a bank account")
            try:
                ac_id = self.context['data']['bank_ac_id']
                if ac_id:
                    bank = BankAccountMaster.objects.get(
                        company=manger.company_id, branches=manger.branches_id, id=ac_id)
                    print("bank object", bank)
                else:
                    bank = None
            except:
                bank = None
        except BankAccountMaster.DoesNotExist:
            bank = None
        try:
            print("checking is there a cash account")
            try:
                cash = CashMaster.objects.get(company=company, branches=branch)
                print("cash object", cash)
            except:
                cash = None
        except CashMaster.DoesNotExist:
            cash = None

        invoice = Invoice(
            **self.validated_data,
            invoice_no=new_recipt_int,
            company=Company.objects.get(id=manger.company_id),
            bank=BankAccountMaster.objects.get(
                branches=manger.branches_id, is_default=True),
            branches=Branches.objects.get(id=manger.branches_id),
            vat=vat,
            cash=cash,
            session=DailySession.objects.get(id=session)
        )
        invoice.save()
        self.instance = invoice
        return self.instance


class ReciptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class ExpenseListSerielizer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['invoice_no', 'total_amt', 'date',
                  'branches', 'ref_no', 'exp_type', 'gross_amt']


class ReciptUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['date', 'qty', 'payment_type', 'fuel',
                  'paid_amt', 'balance_amt', 'total_amt']


class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    # fullname = serializers.CharField(max_length=30)
    # username = serializers.CharField(max_length=30)
    email = serializers.EmailField(max_length=100)
    username = serializers.CharField(max_length=30)
    phone = serializers.CharField(max_length=15)
    # branches = serializers.IntegerField()
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    # password2 = serializers.CharField(style={'input_type': 'password'},write_only=True)

    class Meta:
        model = Employee
        # fields = ['fullname', 'username', 'email', 'phone', 'password', 'password2','id_proof','photo']
        fields = ['phone', 'username', 'password',
                  'email', 'name', 'iqama_no', 'branches']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        print('employee serializer save running')
        manger = BranchManager.objects.get(user=self.context['request'].user)
        password = self.validated_data['password']
        # password2 = self.validated_data['password2']
        # if password != password2:
        #     raise serializers.ValidationError({'error':'Password should be the same'})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError(
                {'error': 'Email id already exists'})

        if Employee.objects.filter(phone=self.validated_data['phone']).exists():
            raise serializers.ValidationError(
                {'error': 'This phone number is already been used'})

        if Employee.objects.filter(phone=self.validated_data['name']).exists():
            raise serializers.ValidationError(
                {'error': 'This employee is already been used'})

        # if Account.objects.filter(username=self.validated_data['username']):
        #     raise serializers.ValidationError({'error':'This username is already been taken'})

        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )

        user.set_password(password)
        user.is_staff = True
        user.is_employee = True
        user.save()
        # branches = Branches.objects.filter(id=self.validated_data['branches']),
        # print("branches================",branches)
        # print("branches================",branches.id)

        employee = Employee(
            user=user,
            company=Company.objects.get(id=manger.company_id),
            phone=self.validated_data['phone'],
            name=self.validated_data['name'],
            iqama_no=self.validated_data['iqama_no'],
            branches=Branches.objects.get(id=manger.branches_id)
        )
        employee.save()
        email_body = 'Hi '+self.validated_data['username'] + \
            ' Use the  username and password to login \n' +\
            'username : '+self.validated_data['email']+'\n' +\
            'password : '+password
        data = {'email_body': email_body, 'to_email': self.validated_data['email'],
                'email_subject': 'User Credentials'}
        Util.send_email(data)

        return employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerielizer(instance.user).data
        return response


class EmployeeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ['user']


class FuelStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelStock
        fields = '__all__'

    def to_representation(self, instance):
        fuels = instance[0]
        print("fuels", fuels.branches)
        print("fuels", fuels.Fuel)
        total_fuel_quantities = FuelMaster.objects.filter(id=fuels.Fuel.id)
        company = Company.objects.filter(id=fuels.company.id)
        branches = Branches.objects.filter(id=fuels.branches.id)
        response = super().to_representation(instance)
        response['qty'] = fuels.qty
        response['Fuel'] = total_fuel_quantities[0].name
        response['company'] = company[0].en_name
        response['branches'] = branches[0].en_name
        return response


class DashboardSerielzer(serializers.ModelSerializer):
    class Meta:
        model = Branches
        fields = ['en_name']

    def to_representation(self, instance):
        balance_amt = Invoice.objects.filter(
            branches=instance.id,).aggregate(Sum('total_amt'))
        total_sale = Invoice.objects.filter(
            branches=instance.id, type=2).aggregate(Sum('total_amt'))
        total_purchase = Invoice.objects.filter(
            branches=instance.id, type=1).aggregate(Sum('total_amt'))
        total_expense = Invoice.objects.filter(
            branches=instance.id, type=3).aggregate(Sum('total_amt'))
        total_sale_by_bank = Invoice.objects.filter(
            branches=instance.id, payment_type=2, type=2).aggregate(Sum('total_amt'))
        # total_fuel_quantities = FuelStock.objects.filter(branches=instance.id)
        # serializer = FuelStockSerializer(total_fuel_quantities)
        # print("fuel stock",serializer.data)

        response = super().to_representation(instance)
        response['total_transactions'] = balance_amt
        response['total_sale'] = total_sale
        response['total_purchase'] = total_purchase
        response['online_sales'] = total_sale_by_bank
        response['total_expense'] = total_expense
        # response['Stock'] = serializer.data
        return response


class ExpenseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

    def save(self):
        print("bank account serielizer running", self.context['data']['type'])
        manger = BranchManager.objects.get(user=self.context['request'].user)
        type = self.context['data']['type']
        branch = Branches.objects.get(id=manger.branches_id)
        ac_id = BankAccountMaster.objects.get(
            branches=manger.branches_id, is_default=True)
        session = self.context['data']['session_id']
        # ac_id=self.context['data']['bank_ac_id']
        print("type=", type)
        last_expense = Invoice.objects.filter(type=3).order_by('id').last()
        # print("last invoice",last_invoice.invoice_no)
        if not last_expense:
            new_expense_int = 1
        else:
            invoice_no = last_expense.invoice_no
            invoice_int = int(invoice_no)
            new_expense_int = invoice_int + 1
            print(last_expense)
            print("New invocie number", new_expense_int)
            print(self.validated_data)
        company = Company.objects.get(id=manger.company_id)
        try:
            print("checking is there a bank account")
            try:
                bank = BankAccountMaster.objects.get(
                    company=company, branches=branch, id=ac_id.id)
                print("bank object", bank)
            except:
                bank = None
        except BankAccountMaster.DoesNotExist:
            bank = None
        try:
            print("checking is there a cash account")
            try:
                cash = CashMaster.objects.get(
                    company=manger.company_id, branches=branch)
                print("cash object", cash)
            except:
                cash = None
        except CashMaster.DoesNotExist:
            cash = None
        invoice = Invoice(
            **self.validated_data,
            invoice_no=new_expense_int,
            session=DailySession.objects.get(id=session),
            company=Company.objects.get(id=manger.company_id),
            branches=Branches.objects.get(id=manger.branches_id),
            bank=bank,
            cash=cash
        )
        invoice.save()
        self.instance = invoice
        return self.instance


class PurchaseReportSerializer(serializers.ModelSerializer):
    # gross_amt_sum = serializers.SerializerMethodField() # add field
    # net_amount_sum = serializers.SerializerMethodField() # add field
    # net_vat_sum = serializers.SerializerMethodField() # add field

    # # payment_type = ChoiceField(choices=Invoice.PAYMENT_TYPE)
    # payment_type = serializers.ChoiceField(choices=Invoice.PAYMENT_TYPE)
    # type = ChoiceField(choices=Invoice.TYPE)
    class Meta:
        model = Invoice
        fields = ['invoice_no', 'date', 'qty', 'payment_type',
                  'total_amt', 'vat_percenatge', 'vat_amount', 'gross_amt']

    def to_representation(self, instance):
        # print("data from view ",self.context['dateto'])
        self.context['request'].user
        response = super().to_representation(instance)
        company_data = CompanySerializer(instance.company).data
        customer_data = CustomerSerializer(instance.contact).data
        kwargs = self.context['data']

        fuel = FuelSerializer(instance.fuel).data
        branch = BranchesSerializer(instance.branches).data
        if instance.payment_type == '1':
            response.pop('payment_type')
            response['invoice_type'] = "Cash"
        elif instance.payment_type == '2':
            response.pop('payment_type')
            response['invoice_type'] = "Online"

        try:
            response['company'] = company_data['user']['username']
            response['Description'] = fuel['name']
            response['suppier_name'] = customer_data['en_name']
            response['price'] = fuel['payable_amt']
            response['branch_name'] = branch['en_name']
            response['Unit'] = "Ltr"

        except TypeError:
            pass

        return response


class DebtorsReportSerializer(serializers.ModelSerializer):
    # payment_type = ChoiceField(choices=Invoice.PAYMENT_TYPE)
    class Meta:
        model = Invoice
        fields = ['invoice_no', 'date', 'contact', 'paid_amt',
                  'total_amt', 'payment_type', 'balance_amt', 'type']

    def to_representation(self, instance):
        # print("data from view ",self.context['dateto'])
        self.context['request'].user
        response = super().to_representation(instance)
        company_data = CompanySerializer(instance.company).data
        customer_data = CustomerSerializer(instance.contact).data

        fuel = FuelSerializer(instance.fuel).data
        if instance.paid_amt:
            response.pop('paid_amt')
            response['recieved'] = instance.paid_amt
        try:
            response['company'] = company_data['user']['username']
            response['fuel'] = fuel['name']
            response['transaction_type'] = "Sales"
            response['customer_name'] = customer_data['en_name']
            response['customer_ar_name'] = customer_data['ar_name']
            response['phone_no'] = customer_data['mobile_no']
            response['UOM'] = "Ltr"

        except TypeError:
            pass
        return response


class SessionListViewSerielizer(serializers.ModelSerializer):
    class Meta:
        model = DailySession
        fields = ['id', 'opening_balance_bank', 'cash_opening_balance',
                  'closing_balance_cash', 'closing_balance_bank', 'status', 'branches']

    def to_representation(self, instance):
        # print("data from view ",self.context['dateto'])
        response = super().to_representation(instance)
        branch = BranchesSerializer(instance.branches).data
        try:
            branch = BranchesSerializer(instance.branches).data
            if instance.branches:
                response.pop('branches')
                response['branch_name'] = branch['en_name']
        except TypeError:
            pass
        return response


class SupplierReportSerializer(serializers.ModelSerializer):
    # payment_type = ChoiceField(choices=Invoice.PAYMENT_TYPE)
    # payment_type = serializers.ChoiceField(choices=Invoice.PAYMENT_TYPE)
    # type = ChoiceField(choices=Invoice.TYPE)
    class Meta:
        model = Invoice
        fields = ['invoice_no', 'date', 'total_amt',
                  'paid_amt', 'balance_amt', 'updated_at']

    def to_representation(self, instance):
        # print("data from view ",self.context['dateto'])
        self.context['request'].user
        response = super().to_representation(instance)
        company_data = CompanySerializer(instance.company).data
        supplier_data = CustomerSerializer(instance.contact).data
        # kwargs=self.context['data']
        # today_min=self.context['datefrom']
        # today_max=self.context['dateto']
        # gross_amt_sum = Invoice.objects.filter(**kwargs,date__range=(today_min, today_max)).aggregate(Sum('gross_amt'))
        # net_amount_sum = Invoice.objects.filter(**kwargs,date__range=(today_min, today_max)).aggregate(Sum('total_amt'))
        # net_amount = Invoice.objects.filter(**kwargs,date__range=(today_min, today_max)).aggregate(Sum('net_amount'))
        # print(gross_amt_sum)
        # print(net_amount_sum)

        # fuel=FuelSerializer(instance.fuel).data
        # if instance.payment_type=='1':
        #     response['payment_type']='Cash'
        # if instance.payment_type=='2':
        #     response['payment_type']='BANK'
        if instance.paid_amt:
            response.pop('paid_amt')
            response['paid'] = instance.paid_amt
        try:
            response['company'] = company_data['user']['username']
            response['transaction_type'] = "purchase"
            response['Supplier'] = supplier_data['en_name']
            # response['gross_amt_sum']=gross_amt_sum['gross_amt__sum']
            # response['net_amount_sum']=net_amount_sum['total_amt__sum']
        except TypeError:
            pass

        return response


class DepositReportSerializer(serializers.ModelSerializer):
    # payment_type = ChoiceField(choices=Invoice.PAYMENT_TYPE)
    class Meta:
        model = Deposit
        fields = '__all__'

    def to_representation(self, instance):
        # print("data from view ",self.context['dateto'])
        self.context['request'].user
        response = super().to_representation(instance)
        owner = OwnerSerializer(instance.owner).data
        bank = BankSerializer(instance.bank).data
        branches = BranchesSerializer(instance.branches).data
        if instance.owner:
            response.pop('owner')
        if instance.branches:
            response.pop('branches')
        try:
            response['owner'] = owner['name']
            response['ac_holder_name'] = bank['acc_holder_name']
            response['ac_number'] = bank['acc_no']
            response['branch'] = branches['en_name']
        except TypeError:
            pass
        return response


class PaymentDueReportSerializer(serializers.ModelSerializer):
    # payment_type = ChoiceField(choices=Invoice.PAYMENT_TYPE)
    class Meta:
        model = Invoice
        fields = ['invoice_no', 'date', 'contact', 'paid_amt',
                  'total_amt', 'payment_type', 'balance_amt', 'type']

    def to_representation(self, instance):
        # print("data from view ",self.context['dateto'])
        self.context['request'].user
        response = super().to_representation(instance)
        company_data = CompanySerializer(instance.company).data
        customer_data = CustomerSerializer(instance.contact).data

        fuel = FuelSerializer(instance.fuel).data
        if instance.paid_amt:
            response.pop('paid_amt')
            response['recieved'] = instance.paid_amt
        if instance.type:
            response.pop('type')
        try:
            response['company'] = company_data['user']['username']
            response['fuel'] = fuel['name']
            response['transaction_type'] = "Sales"
            response['contact_en_name'] = customer_data['en_name']
            response['contact_ar_name'] = customer_data['ar_name']
            response['phone_no'] = customer_data['mobile_no']
            response['UOM'] = "Ltr"

        except TypeError:
            pass
        return response


class IncomeReportSerializer(serializers.ModelSerializer):
    # payment_type = ChoiceField(choices=Invoice.PAYMENT_TYPE)
    class Meta:
        model = Invoice
        fields = ['total_amt', 'contact', 'type', 'date']

    def to_representation(self, instance):
        self.context['request'].user
        response = super().to_representation(instance)
        customer_data = CustomerSerializer(instance.contact).data
        if instance.contact:
            response.pop('contact')
        try:
            response['contact'] = customer_data['en_name']
            response['um'] = "Ltr"

        except TypeError:
            pass

        return response


class SupplierListSerielizer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'en_name']


class ExpenseReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = ['date', 'payment_type', 'gross_amt', 'paid_amt',
                  'total_amt', 'invoice_no', 'exp_type', 'ref_no']

    def to_representation(self, instance):
        # print("data from view ",self.context['dateto'])
        self.context['request'].user
        response = super().to_representation(instance)
        company_data = CompanySerializer(instance.company).data
        customer_data = CustomerSerializer(instance.contact).data
        branch = BranchesSerializer(instance.branches).data
        if instance.payment_type == '1':
            response.pop('payment_type')
            response['payment_type'] = "Cash"
        elif instance.payment_type == '2':
            response.pop('payment_type')
            response['payment_type'] = "Online"
        try:
            response['username'] = company_data['user']['username']
            response['customer'] = customer_data['en_name']
            response['branch'] = branch['en_name']
        except TypeError:
            pass

        return response


class MeterReadingReporSerielizer(serializers.ModelSerializer):

    class Meta:
        model = MeterReading
        fields = ['date', 'branches', 'start_reading', 'end_reading',
                  'payable_amt', 'fuel', 'fuel_stock', 'employee']

    def to_representation(self, instance):
        # print("data from view ",self.context['dateto'])
        self.context['request'].user
        response = super().to_representation(instance)
        dispence = DispenceSerializer(instance.dispence).data
        fuel = FuelSerializer(instance.fuel).data
        employee = EmployeeSerializer(instance.employee).data
        branch = BranchesSerializer(instance.branches).data
        if instance.branches:
            response.pop('branches')
        elif instance.employee:
            response.pop('employee')
        try:
            response['dispencer'] = dispence['name']
            response['fuel'] = fuel['name']
            response['UOM'] = "Ltr"
            response['branch'] = branch['en_name']
            response['employee_name'] = employee['name']

        except TypeError:
            pass

        return response


class PaymentInReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = ['invoice_no', 'date', 'qty', 'payment_type',
                  'total_amt', 'vat_percenatge', 'vat_amount', 'gross_amt']

    def to_representation(self, instance):
        # print("data from view ",self.context['dateto'])
        self.context['request'].user
        response = super().to_representation(instance)
        company_data = CompanySerializer(instance.company).data
        customer_data = CustomerSerializer(instance.contact).data
        kwargs = self.context['data']

        fuel = FuelSerializer(instance.fuel).data
        branch = BranchesSerializer(instance.branches).data
        if instance.payment_type == '1':
            response.pop('payment_type')
            response['invoice_type'] = "Cash"
        elif instance.payment_type == '2':
            response.pop('payment_type')
            response['invoice_type'] = "Online"
        try:
            response['company'] = company_data['user']['username']
            response['Description'] = fuel['name']
            response['supplier_name'] = customer_data['en_name']
            response['price'] = fuel['payable_amt']
            response['branch_name'] = branch['en_name']
            response['phone_no'] = customer_data['mobile_no']
            response['Unit'] = "Ltr"

        except TypeError:
            pass

        return response


class PaymentOutReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = ['date', 'qty', 'payment_type', 'gross_amt',
                  'vat_amount', 'total_amt', 'vat_percenatge', 'invoice_no']

    def to_representation(self, instance):
        # print("data from view ",self.context['dateto'])
        self.context['request'].user
        response = super().to_representation(instance)
        company_data = CompanySerializer(instance.company).data
        customer_data = CustomerSerializer(instance.contact).data
        fuel = FuelSerializer(instance.fuel).data
        branch = BranchesSerializer(instance.branches).data
        if instance.payment_type == '1':
            response.pop('payment_type')
            response['payment_type'] = "Cash"
        elif instance.payment_type == '2':
            response.pop('payment_type')
            response['payment_type'] = "Online"
        try:
            response['username'] = company_data['user']['username']
            response['description'] = fuel['name']
            response['price'] = fuel['payable_amt']
            response['customer'] = customer_data['en_name']
            response['phone_no'] = customer_data['mobile_no']
            response['um'] = "Ltr"
            response['branch'] = branch['en_name']

        except TypeError:
            pass

        return response


class FuelStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelStock
        fields = '__all__'


class FuelStockCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelStock
        fields = '__all__'

    def save(self):
        manger = BranchManager.objects.get(user=self.context['request'].user)
        # print("dta in ",)
        # breakpoint()
        conatct = FuelStock(
            **self.validated_data,
            branches=Branches.objects.get(id=manger.branches_id),
            company=Company.objects.get(id=manger.company_id)
        )
        conatct.save()
        return conatct


class SessionReportSerializer(serializers.ModelSerializer):
    # payment_type = ChoiceField(choices=Invoice.PAYMENT_TYPE)
    class Meta:
        model = DailySession
        fields = ['id', 'date', 'branches', 'opening_balance_bank', 'cash_opening_balance',
                  'closing_balance_bank', 'closing_balance_cash', 'total_transactions']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        branch_data = BranchesSerializer(instance.branches).data

        if instance.branches:
            response.pop('branches')
        try:
            response['branch_name'] = branch_data['en_name']

        except TypeError:
            pass
        return response


class CashMasterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashMaster
        fields = '__all__'


class SessionAccountReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountLedger
        fields = ['id', 'balance', 'debit_balance', 'credit_balance',
                  'bank', 'cash', 'total_transactions', 'total_sales', 'total_purchase', 'total_expense']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        bank_data = BankAccountListSerielizer(instance.bank).data
        cash_data = CashMasterListSerializer(instance.cash).data
        if instance.bank:
            response.pop('bank')
        if instance.cash:
            response.pop('cash')
        try:
            response['bank_ac_holder_name'] = bank_data['acc_holder_name']
            response['account_no'] = bank_data['acc_no']
            response['cash_ac_name'] = cash_data['cash_ac_name']

        except TypeError:
            pass
        return response


class ChangePasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        print("validated data", self.validated_data)
        password = self.validated_data['password']
        email = self.validated_data['email']
        print("Password in Request", password)
        print("Email", email)
        if email:
            user = User.objects.filter(email=self.validated_data['email'])
            print("User forund", user)
            user = user[0]
            user.set_password(password)
            user.save()
            return
        else:
            raise serializers.ValidationError({'error': 'invlaid email'})
