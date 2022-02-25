from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from administrator.models import BranchManager, Company, Employee, User


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
        token['branch_user_company_id'] = Company.objects.values('user').get(id=BranchManager.objects.values(
            'company_id').get(user=user).get('company_id')) if user.is_branch_user else None
        token['branch_tenant_name'] = User.objects.values('username').get(
            id=token['branch_user_company_id']['user']) if user.is_branch_user else None

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
            'company_id').get(user=self.user).get('company_id')) if self.user.is_employee else None})
        data.update({'branch_user_company_id': Company.objects.values('user').get(id=BranchManager.objects.values(
            'company_id').get(user=self.user).get('company_id')) if self.user.is_branch_user else None})
        data.update({'emp_tenant_name': User.objects.values('username').get(
            id=data['emp_company_user_id']['user']) if self.user.is_employee else None})
        data.update({'branch_user_tenant_name': User.objects.values('username').get(
            id=data['branch_user_company_id']['user']) if self.user.is_branch_user else None})
        return data


# class ComapanyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['username']=user.username
#         token['is_admin'] = user.is_admin
#         token['is_company'] = user.is_company
#         token['is_superuser'] = user.is_superuser
#         token['is_employee'] = user.is_employee
#         token['is_branch_user'] = user.is_branch_user
#         token['company_id'] = Company.objects.values('id').get(user=user).get('id') if user.is_company else None
#         token['employee_compnay_id'] = Employee.objects.values('id','company_id').get(user=user).get('id') if user.is_employee else None
#         token['tenant_name'] = User.objects.values('username').get(id=user.id)
#         # if user.is_employee else None
#         # print("token insfo",token)
#         return token
#     def validate(self, attrs):
#         # company= Employee.objects.values('company_id').get(user=self.user)
#         # print(company)
#         # if self.user.is_employee:
#         #    empl=Employee.objects.get(user=self.user)
#         #    print(empl.company_id)
#         #    company=Company.objects.values('id').get(user=self.user).get('id')
#         data = super(ComapanyTokenObtainPairSerializer, self).validate(attrs)
#         data.update({'username': self.user.username})
#         data.update({'is_admin': self.user.is_super_admin})
#         data.update({'is_company': self.user.is_company})
#         data.update({'is_employee': self.user.is_employee})
#         data.update({'is_superuser': self.user.is_superuser})
#         data.update({'is_branch_user': self.user.is_branch_user})
#         data.update({'company_id': Company.objects.values('id').get(user=self.user).get('id') if self.user.is_company else None})
#         data.update({'emp_company_user_id': Company.objects.values('user').get(id=Employee.objects.values('company_id').get(user=self.user).get('company_id')) if self.user.is_employee else None})
#         data.update({'emp_tenant_name':User.objects.values('username').get(id=data['emp_company_user_id']['user']) if self.user.is_employee else None })
#         return data
