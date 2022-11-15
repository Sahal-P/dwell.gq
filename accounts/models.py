from email.policy import default
from enum import unique
from pyexpat import model
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid
from category.models import Products
# Create your models here.

class MyAccountManager(BaseUserManager):
    use_in_migrations: True
    def create_user(self,first_name,last_name,username,email,phone_number, password=None , **extra_fields):
        if not email:
            raise ValueError('Email is required')
        
        if not username:
            raise ValueError('user must have username')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            phone_number =phone_number, **extra_fields
        )
        user.is_active = True
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name, last_name,email, phone_number, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username= username,
            password = password,
            first_name = first_name,
            last_name = last_name,
            phone_number=phone_number,
        )
        
        user.is_admin = True
        user.is_active = True
        user.is_staff = True    
        user.is_superuser = True
        user.save(using=self._db)
        return user
        


class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length = 50)
    last_name       = models.CharField(max_length =50)
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    phone_number    = models.CharField(max_length=50)
    
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    is_blocked      = models.BooleanField(default=False)
    
    objects = MyAccountManager()

    
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name','phone_number']
    
    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True

class Address(models.Model):
    user = models.ForeignKey(Account, on_delete= models.CASCADE)
    first_name      = models.CharField(max_length = 50)
    last_name       = models.CharField(max_length =50,null = True, blank=True)
    email           = models.EmailField(max_length=100, null = True, blank=True)
    phone_number_1  = models.CharField(max_length=50)
    phone_number_2  = models.CharField(max_length=50, null = True, blank=True)
    address_1       = models.TextField(blank=False)
    address_2       = models.TextField(null= True, blank=True)
    country         = models.CharField(max_length=50, blank=False)
    State           = models.CharField(max_length=50, blank=False)
    zip_code        = models.IntegerField(blank=False)

class Wishlist(models.Model):
    user            = models.ForeignKey(Account,on_delete=models.CASCADE)
    wished_item     = models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity        = models.IntegerField(null=True,blank=True)
    added_date      = models.DateTimeField(auto_now_add=True)
    
   