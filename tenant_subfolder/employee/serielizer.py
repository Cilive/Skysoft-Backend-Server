
from datetime import datetime
from rest_framework import serializers
from company.models import BankAccountMaster, CashMaster, DailySession, Dispence, FuelMaster, FuelStock, Invoice, MeterReading, VatMaster
from administrator.models import Branches, Company, Employee, User
from django.db.models import Q
import base64
from fatoora import Fatoora

from administrator.serielizer import CompanySerializer, EmployeeSerializer, UserSerielizer


# class InvoiceGenerateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Invoice
#         fields = '__all__'
#         # fields = ('id', 'invoice_no','gross_amt','fuel','qty','type' )


#     def save(self):
#         last_invoice = Invoice.objects.filter(Q(type=2) ).order_by('id').last()
#         print("last invoice",last_invoice.invoice_no)
#         if not last_invoice:
#             new_invoice_int= 1
#         else:
#             invoice_no = last_invoice.invoice_no
#             invoice_int = int(invoice_no)
#             new_invoice_int = invoice_int + 1

#         print(last_invoice)
#         print("New invocie number",new_invoice_int)
#         print(self.validated_data)

#         emp=Employee.objects.get(user=self.context['request'].user)

#         invoice = Invoice(
#             **self.validated_data,
#             invoice_no=new_invoice_int,
#             emp = Employee.objects.get(user=self.context['request'].user),
#             company = Company.objects.get(id=emp.company_id)
#         )
#         invoice.save()
#         self.instance = invoice
#         return self.instance
def utf8len(s):
    return len(s.encode('utf-8'))


class InvoiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

    def save(self):
        print("bank account serielizer running", self.context['data']['type'])
        # print("Branches in  serielizer running",self.context['data']['branches'])
        type = self.context['data']['type']
        session = self.context['data']['session_id']

        # branch=self.context['data']['branches']
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

        # need to get the employee correspnding company
        emp = Employee.objects.get(user=self.context['request'].user)
        print("employee logged in", emp)

        company = Company.objects.get(id=emp.company_id)
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

        try:
            print("checking is there a bank account")
            try:
                # ac_id=self.context['data']['bank_ac_id']
                # if ac_id:
                #    bank=BankAccountMaster.objects.get(company=company,branches=emp.branches,id=ac_id)
                #    print("bank object",bank)
                # ac_id=self.context['data']['bank_ac_id']
                # ac_id=self.context['data']['bank_ac_id']

                bank = BankAccountMaster.objects.get(
                    company=company, branches=emp.branches, is_default=True)
            except:
                bank = None
        except BankAccountMaster.DoesNotExist:
            bank = None

        try:
            print("checking is there a cash account")
            try:
                cash = CashMaster.objects.get(
                    company=emp.company_id, branches=emp.branches_id)
                print("cash object", cash)
            except:
                cash = None
        except CashMaster.DoesNotExist:
            cash = None

        invoice = Invoice(
            **self.validated_data,
            invoice_no=new_invoice_int,
            emp=Employee.objects.get(user=self.context['request'].user),
            company=Company.objects.get(id=emp.company_id),
            branches=Branches.objects.get(id=emp.branches_id),
            bank=bank,
            cash=cash,
            base_64_encoded=fatoora_obj.base64,
            session=DailySession.objects.get(id=session)

        )
        invoice.save()
        print("===============invoice created succesfully==========", invoice)
        self.instance = invoice
        return self.instance


class MeterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeterReading
        fields = '__all__'

    def save(self):
        emp = Employee.objects.get(user=self.context['request'].user)
        fuelstock = FuelStock.objects.get(
            Fuel=self.validated_data['fuel'], branches=emp.branches_id)
        print("fuelstock", fuelstock.qty)
        meter_reading = MeterReading(
            **self.validated_data,
            company=Company.objects.get(id=emp.company_id),
            branches=Branches.objects.get(id=emp.branches_id),
            employee=Employee.objects.get(user=self.context['request'].user),
            fuel_stock=fuelstock.qty
        )
        meter_reading.save()
        return meter_reading


class MeterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeterReading
        fields = '__all__'


class FuelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelMaster
        fields = '__all__'


class VatSerializer(serializers.ModelSerializer):
    class Meta:
        model = VatMaster
        fields = '__all__'


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccountMaster
        fields = '__all__'


class DispenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispence
        fields = '__all__'

    def to_representation(self, instance):
        # print("data in self",self.context['data'])
        data = super(DispenceSerializer, self).to_representation(instance)
        data['dispencer_count'] = self.context['data']
        return data


class BranchSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(style={'input_type': 'password'},write_only=True)
    class Meta:
        model = Branches
        fields = ['en_name', 'ar_name', 'vat_no', 'cr_no', 'lan_no', 'phone']

    def to_representation(self, instance):
        data = super(BranchSerializer, self).to_representation(instance)
        # data['user'] = UserSerielizer(instance.user).data
        data['company'] = CompanyNameSerielizer(instance.company).data
        return data


class CompanyNameSerielizer(serializers.ModelSerializer):
    # password = serializers.CharField(style={'input_type': 'password'},write_only=True)

    class Meta:
        model = Company
        fields = ['en_name', 'ar_name', 'vat_no', 'cr_no', 'lan_no', 'phone']


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
