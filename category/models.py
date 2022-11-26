
from email.policy import default
from django.utils import timezone
from django.db import models

import datetime


# Create your models here.


class Category(models.Model):
    category_name       = models.CharField(max_length = 50, unique=True)
    slug                = models.CharField(max_length=100, unique=True)
    cata_img            = models.ImageField(upload_to ='imgs/category_img',blank =True, null = True)
   
    def __str__(self):
        return self.category_name
    
class SubCategory(models.Model):
    subcategory_name    = models.CharField(max_length = 50 , unique=True)
    Sub_slug            = models.CharField(max_length =50, unique=True)
    Sub_img             = models.ImageField(upload_to ='imgs/sub_category_img', blank = True, null = True)
    category            = models.ForeignKey(Category, on_delete =models.CASCADE)
    
    def __str__(self):
        return self.subcategory_name
    
class Products(models.Model):
    product_name        = models.CharField(max_length = 50, unique=True)
    slug                = models.CharField(max_length=100, unique=True)
    brand               = models.TextField(max_length = 255, blank = True)
    description         = models.TextField(max_length = 255, blank = True)
    quantity            = models.IntegerField(null= False , blank = True)
    original_price      = models.FloatField(null= False, blank = True )
    selling_price       = models.FloatField(null= False , blank = True) 
    product_img1        = models.ImageField(upload_to ='imgs/product_img',blank =True, null = True)
    product_img2        = models.ImageField(upload_to ='imgs/product_img',blank =True, null = True)
    product_img3        = models.ImageField(upload_to ='imgs/product_img',blank =True, null = True)
    product_img4        = models.ImageField(upload_to ='imgs/product_img',blank =True, null = True)
    added_Date          = models.DateField(auto_now_add=True , null = True)
    status              = models.BooleanField(default=False)
    category            = models.ForeignKey(Category, on_delete =models.CASCADE)
    subcategory         = models.ForeignKey(SubCategory, on_delete = models.CASCADE)
  
    def __str__(self):
        return self.product_name