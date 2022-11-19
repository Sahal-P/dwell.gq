from django.db import models
from category.models import *
from accounts.models import Account
# Create your models here.

class Cart(models.Model):
    cart_id         = models.CharField(max_length = 250, blank=True)
    date_added      = models.DateField(auto_now_add = True)
    
    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    user            = models.ForeignKey(Account, on_delete=models.CASCADE ,null =True)
    product         = models.ForeignKey(Products, on_delete = models.CASCADE)
    cart            = models.ForeignKey(Cart, on_delete = models.CASCADE, null =True)
    Quantity        = models.IntegerField()
    is_active       = models.BooleanField(default=True)
    
    def sub_total(self):
        return self.product.selling_price *self.Quantity
    
    def __str__(self):
        return self.product
    
class OldCart(models.Model):
    user            = models.ForeignKey(Account, on_delete=models.CASCADE ,null =True)
    product         = models.ForeignKey(Products, on_delete = models.CASCADE)
    cart            = models.ForeignKey(Cart, on_delete = models.CASCADE, null =True)
    Quantity        = models.IntegerField()
    date_added      = models.DateField(auto_now_add = True ,null = True)
    
    def __str__(self):
        return self.user