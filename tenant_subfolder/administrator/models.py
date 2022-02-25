import os
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager,PermissionsMixin)
from django.utils.translation import gettext_lazy as _


# Create your models here.
class UserManager(BaseUserManager):
        def create_user(self, username, email, password=None):
            if username is None:
                raise TypeError('Users should have a username')
            if email is None:
                raise TypeError('Users should have a Email')
            user=self.model(username=username, email=self.normalize_email(email))
            user.set_password(password)
            user.save()      
            return user

        def create_superuser(self, username, email, password=None):
            if password is None:
                raise TypeError('Password should not be none')
            user=self.create_user(username,email,password)
            user.is_superuser=True
            user.is_staff=True
            user.save()
            return user


class User(AbstractBaseUser,PermissionsMixin):
    username=models.CharField(max_length=255,unique=True,db_index=True)
    email=models.EmailField(max_length=255,unique=True,db_index=True)
    phone = models.CharField(max_length=15,db_index=True,null=True,blank=True,)
    is_company=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_employee = models.BooleanField(default=False)
    is_branch_user = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_super_admin = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    objects=UserManager()

    def __str__(self) -> str:
        return self.email

    def tokens(self):
        return ''

def get_image_path(instance, filename):
    return 'media/{filename}'.format(filename=filename)
class Company(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_id')
    en_name = models.CharField(max_length=30)
    ar_name = models.CharField(max_length=30)
    en_place = models.CharField(max_length=30)
    ar_place = models.CharField(max_length=30)
    en_district = models.CharField(max_length=30)
    ar_district = models.CharField(max_length=30)
    cr_no = models.CharField(max_length=15)
    vat_no = models.CharField(max_length=15)
    lan_no = models.CharField(max_length=15)
    logo = models.ImageField(_("logo"),upload_to =get_image_path, null=True,blank=True)
    status = models.BooleanField(default=True)
    phone = models.CharField(max_length=15,unique=True)
    branch_count = models.IntegerField(null=True,blank=True)
    
    class Meta:
        db_table = 'company'
        
    def __str__(self):
        return self.en_name
class Branches(models.Model):
    en_name = models.CharField(max_length=30)
    ar_name = models.CharField(max_length=30)
    en_place = models.CharField(max_length=30)
    ar_place = models.CharField(max_length=30)
    en_district = models.CharField(max_length=30)
    ar_district = models.CharField(max_length=30)
    cr_no = models.CharField(max_length=15)
    vat_no = models.CharField(max_length=15)
    lan_no = models.CharField(max_length=15)
    logo = models.ImageField(upload_to ='media/', null=True)
    status = models.BooleanField(default=True)
    phone = models.CharField(max_length=15,unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'branches'
        
    def __str__(self):
        return self.en_name

class Employee(models.Model):
    branches=models.ForeignKey(Branches, on_delete=models.CASCADE, null=True)                              

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='employee_id')
    company= models.ForeignKey(Company, on_delete=models.CASCADE,
                            null=True, related_name='company_id')
    name = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=15,null=True)
    iqama_no=models.CharField(max_length=15,null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'employee'


class BranchManager(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,null=True,related_name='branch_manager_id' )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    branches=models.ForeignKey(Branches, on_delete=models.CASCADE, related_name='branches_id', null=True)                              
    name = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=15,unique=True)
    iqama_no=models.CharField(max_length=15,unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'branch_manager'
    
class OtpExpiry(models.Model):
    otp =models.IntegerField(unique=True)
    expiry = models.TimeField( null=True)
    current_time = models.TimeField( null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'otp_expiry'
        

def get_upload_path(instance, filename):
    return 'media/{filename}'.format(filename=filename)

class ProfileImages(models.Model):
    logo = models.ImageField(_("logo"),upload_to =get_upload_path, null=True,blank=True)
    
    def __str__(self):
        return self.logo
    
    class Meta:
        db_table = 'profile_pictures'

