from distutils.log import error
from logging import exception
from rest_framework.response import Response
from rest_framework import status

from django.db import models
from datetime import datetime, timedelta
import random


# from administrator.models import BankAccountMaster
from .models import BranchManager, Branches, Employee, OtpExpiry, ProfileImages, User, Company
from customers.models import Client, Domain
from rest_framework import serializers
from .utils import Util
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ComapanyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['is_admin'] = user.is_admin
        token['is_company'] = user.is_company
        token['is_superuser'] = user.is_superuser
        token['is_employee'] = user.is_employee
        token['is_branch_user'] = user.is_branch_user
        token['company_id'] = Company.objects.values('id').get(
            user=user).get('id') if user.is_company else None
        token['employee_compnay_id'] = Employee.objects.values(
            'id', 'company_id').get(user=user).get('id') if user.is_employee else None
        token['tenant_name'] = User.objects.values('username').get(id=user.id)
        # if user.is_employee else None
        # print("token insfo",token)
        return token

    def validate(self, attrs):
        # company= Employee.objects.values('company_id').get(user=self.user)
        # print(company)
        # if self.user.is_employee:
        #    empl=Employee.objects.get(user=self.user)
        #    print(empl.company_id)
        #    company=Company.objects.values('id').get(user=self.user).get('id')
        data = super(ComapanyTokenObtainPairSerializer, self).validate(attrs)
        data.update({'username': self.user.username})
        data.update({'is_admin': self.user.is_super_admin})
        data.update({'is_company': self.user.is_company})
        data.update({'is_employee': self.user.is_employee})
        data.update({'is_superuser': self.user.is_superuser})
        data.update({'is_branch_user': self.user.is_branch_user})
        data.update({'company_id': Company.objects.values('id').get(
            user=self.user).get('id') if self.user.is_company else None})
        data.update({'emp_company_user_id': Company.objects.values('user').get(id=Employee.objects.values(
            'id', 'company_id').get(user=self.user).get('id')) if self.user.is_employee else None})
        data.update({'emp_tenant_name': User.objects.values('username').get(
            id=data['emp_company_user_id']['user']) if self.user.is_employee else None})
        # print("Logged in user is a company/owner",data['is_company'])
        # # if data['is_company']:
        # #     print("the logged in user is admin/company")
        # #     print("self.user",self.user.id)
        # #     company=Company.objects.get(user=self.user)
        # #     print("company data",company)
        # #     if company:
        # #         bank_account=BankAccountMaster.objects.get(company=company)
        # #         print("company have filled account details")

        return data


class UserSerielizer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

        # fields='__all__'


class CompanyRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=30)
    email = serializers.EmailField(max_length=100)
    phone = serializers.CharField(max_length=15)
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    en_name = serializers.CharField(max_length=30)
    ar_name = serializers.CharField(max_length=30)
    en_place = serializers.CharField(max_length=30)
    ar_place = serializers.CharField(max_length=30)
    en_district = serializers.CharField(max_length=30)
    ar_district = serializers.CharField(max_length=30)
    cr_no = serializers.CharField(max_length=15)
    vat_no = serializers.CharField(max_length=15)
    lan_no = serializers.CharField(max_length=15)
    logo = serializers.ImageField(
        max_length=None, use_url=True, allow_null=True, required=False)
    branch_count = serializers.IntegerField()

    class Meta:
        model = Company
        # fields = ['fullname', 'username', 'email', 'phone', 'password', 'password2','id_proof','photo']
        fields = ['en_name', 'ar_name', 'en_place', 'ar_place', 'en_district', 'ar_district',
                  'cr_no', 'vat_no', 'lan_no', 'email', 'phone', 'password', 'logo', 'username', 'branch_count']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        try:
            print("validated data", self.validated_data)
            password = self.validated_data['password']

            user = User(
                username=self.validated_data['username'],
                email=self.validated_data['email']
            )
            user.set_password(password)
            user.is_company = True
            user.is_admin = True
            user.save()

            # self.validated_data.pop('phone')
            # self.validated_data.pop('email')
            # self.validated_data.pop('password')
            # print(self.validated_data['email'])

            company = Company(
                user=user,
                en_name=self.validated_data['en_name'],
                ar_name=self.validated_data['ar_name'],
                en_place=self.validated_data['en_place'],
                ar_place=self.validated_data['ar_place'],
                en_district=self.validated_data['en_district'],
                ar_district=self.validated_data['ar_district'],
                cr_no=self.validated_data['cr_no'],
                vat_no=self.validated_data['vat_no'],
                lan_no=self.validated_data['lan_no'],
                logo=self.validated_data['logo'],
                phone=self.validated_data['phone'],
                branch_count=self.validated_data['branch_count']
            )
            company.save()
            # breakpoint()
            print("User Obeject after creating user===============>", user.is_company)
            tenant = Client(schema_name=user.username,
                            name=user.username,
                            )
            tenant.save()
            domain = Domain(
                # domain=tenant.name+'.localhost',
                domain=tenant.name,
                is_primary=True,
                tenant=tenant,
            )
            domain.save()
        except Exception as e:
            print("Exception in creating company", e)
            user.delete()
            raise e
        email_body = 'Hi '+self.validated_data['username'] + \
            ' Use the link below username and password to login \n' +\
            'username : '+self.validated_data['email']+'\n' +\
            'password : '+password
        data = {'email_body': email_body, 'to_email': self.validated_data['email'],
                'email_subject': 'Verify your email'}
        Util.send_email(data)
        return company


class CompanySerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Company
        fields = '__all__'

    def to_representation(self, instance):
        data = super(CompanySerializer, self).to_representation(instance)
        data['user'] = UserSerielizer(instance.user).data
        return data


class CompanyUpdationSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=15)
    en_name = serializers.CharField(max_length=30)
    ar_name = serializers.CharField(max_length=30)
    en_place = serializers.CharField(max_length=30)
    ar_place = serializers.CharField(max_length=30)
    en_district = serializers.CharField(max_length=30)
    ar_district = serializers.CharField(max_length=30)
    cr_no = serializers.CharField(max_length=15)
    vat_no = serializers.CharField(max_length=15)
    lan_no = serializers.CharField(max_length=15)
    logo = serializers.ImageField(
        max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = Company
        # fields = ['fullname', 'username', 'email', 'phone', 'password', 'password2','id_proof','photo']
        fields = ['en_name', 'ar_name', 'en_place', 'ar_place', 'en_district', 'ar_district',
                  'cr_no', 'vat_no', 'lan_no', 'logo', 'phone']


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
            email=self.validated_data['email'],
            mobile_no=self.validated_data['phone']
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
            company=Company.objects.get(user=self.context['request'].user),
            phone=self.validated_data['phone'],
            name=self.validated_data['name'],
            iqama_no=self.validated_data['iqama_no'],
            branches=self.validated_data['branches']
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
        exclude = ('user',)


class BranchesRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branches
        fields = '__all__'

    def save(self):
        branch = Branches(
            **self.validated_data,
            company=Company.objects.get(user=self.context['request'].user)
        )
        branch.save()
        return branch


class BranchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branches
        fields = '__all__'


class BranchManagerRegistrationSerializer(serializers.ModelSerializer):
    # fullname = serializers.CharField(max_length=30)
    # username = serializers.CharField(max_length=30)
    email = serializers.EmailField(max_length=100)
    username = serializers.CharField(max_length=30)
    phone = serializers.CharField(max_length=15)
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    # password2 = serializers.CharField(style={'input_type': 'password'},write_only=True)

    class Meta:
        model = BranchManager
        # fields = ['fullname', 'username', 'email', 'phone', 'password', 'password2','id_proof','photo']
        fields = ['phone', 'username', 'password',
                  'email', 'name', 'iqama_no', 'branches']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        password = self.validated_data['password']

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError(
                {'error': 'Email id already exists'})

        if BranchManager.objects.filter(phone=self.validated_data['phone']).exists():
            raise serializers.ValidationError(
                {'error': 'This phone number is already been used'})

        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )

        user.set_password(password)
        user.is_staff = True
        user.is_branch_user = True
        user.save()
        print("user id", user.id)
        print("user id", user.email)

        branch_user = BranchManager(
            user=user,
            company=Company.objects.get(user=self.context['request'].user),
            phone=self.validated_data['phone'],
            name=self.validated_data['name'],
            iqama_no=self.validated_data['iqama_no'],
            branches=self.validated_data['branches']

        )
        branch_user.save()
        email_body = 'Hi '+self.validated_data['username'] + \
            ' Use the  username and password to login \n' +\
            'username : '+self.validated_data['email']+'\n' +\
            'password : '+password
        data = {'email_body': email_body, 'to_email': self.validated_data['email'],
                'email_subject': 'User Credentials'}
        Util.send_email(data)

        return branch_user


class BranchManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchManager
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerielizer(instance.user).data
        return response


class PasswordChangeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100)

    class Meta:
        model = User
        # fields = ['fullname', 'username', 'email', 'phone', 'password', 'password2','id_proof','photo']
        fields = ['email']
        # extra_kwargs = {
        #     'password':{'write_only':True}
        # }

    def save(self):
        print("validated data", self.validated_data)
        password = self.validated_data['email']
        otp = random.randint(1000, 9999)
        print("Random number generated", otp)

        email_body = ' Use the OTP below to change password  \n' +\
            'OTP : '+str(otp)+''
        data = {'email_body': email_body, 'to_email': self.validated_data['email'],
                'email_subject': 'Skysoft change password'}
        Util.send_email(data)
        now = datetime.now()
        now_plus_10 = now + timedelta(minutes=10)
        expiry = now_plus_10
        print("current time", now)
        print("Expiry time generated", expiry)
        # breakpoint()
        Otp = OtpExpiry(
            # domain=tenant.name+'.localhost',
            otp=otp,
            expiry=expiry,
            current_time=now,
        )
        Otp.save()
        return

        # if User.objects.filter(email=self.validated_data['email']).exists():
        #     raise serializers.ValidationError({'error':'Email id already exists'})

        # if Company.objects.filter(phone=self.validated_data['phone']).exists():
        #     raise serializers.ValidationError({'error':'This phone number is already been used'})

        # # breakpoint()
        # user = User(
        #     username = self.validated_data['username'],
        #     email = self.validated_data['email']
        # )
        # user.set_password(password)
        # user.is_company = True
        # user.is_admin = True
        # user.save()

        # # self.validated_data.pop('phone')
        # # self.validated_data.pop('email')
        # # self.validated_data.pop('password')
        # # print(self.validated_data['email'])

        # company = Company(
        #     user= user,
        #     en_name = self.validated_data['en_name'],
        #     ar_name = self.validated_data['ar_name'],
        #     en_place = self.validated_data['en_place'],
        #     ar_place = self.validated_data['ar_place'],
        #     en_district = self.validated_data['en_district'],
        #     ar_district = self.validated_data['ar_district'],
        #     cr_no = self.validated_data['cr_no'],
        #     vat_no = self.validated_data['vat_no'],
        #     lan_no = self.validated_data['lan_no'],
        #     logo = self.validated_data['logo'],
        #     phone = self.validated_data['phone']
        # )
        # company.save()

        # print("User Obeject after creating user===============>",user.is_company)
        # tenant = Client(schema_name=user.username,
        #     name=user.username,
        #     )
        # tenant.save()
        # domain = Domain(
        #     # domain=tenant.name+'.localhost',
        #     domain=tenant.name,
        #     is_primary=True,
        #     tenant=tenant,
        #     )
        # domain.save()
        # return company


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
        otp = self.context['request'].data['otp']
        print("Password in Request", password)
        print("OTP in Request", otp)
        now = datetime.now()
        now_plus_10 = now + timedelta(minutes=10)
        expiry = now_plus_10
        otp_valid = OtpExpiry.objects.filter(
            otp=otp, expiry__gte=now, current_time__lte=now_plus_10).exists()
        print("current time", now)
        print("Expiry time generated", expiry)
        if otp_valid:
            print("OTP is valid", otp_valid)
            user = User.objects.filter(email=self.validated_data['email'])
            print("User forund", user)
            user = user[0]
            user.set_password(password)
            user.save()
            return
        else:
            raise serializers.ValidationError({'error': 'OTP is invlaid'})


class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImages
        fields = '__all__'
