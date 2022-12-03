from django.db import models
from category.models import *
from accounts.models import Account
# Create your models here.

class GCart(models.Model):
    Guest_id         = models.CharField(max_length = 250, blank=True)
    date_added      = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.Guest_id
    
class CartItem(models.Model):
    user            = models.ForeignKey(Account, on_delete=models.CASCADE ,null =True)
    product         = models.ForeignKey(Products, on_delete = models.CASCADE)
    Guest           = models.ForeignKey(GCart, on_delete = models.CASCADE, null =True)
    Quantity        = models.IntegerField()
    is_active       = models.BooleanField(default=True)
    
    def sub_total(self):
        if self.product.offer_price is not None:
            return self.product.offer_price *self.Quantity
        else:
            return self.product.selling_price *self.Quantity
    def sub_total_c(self,coupen_didected):
        if self.product.offer_price is not None:
            if coupen_didected is not 0:
                return self.product.offer_price *self.Quantity-coupen_didected 
            else:
                return self.product.offer_price *self.Quantity
        else:
            return self.product.selling_price *self.Quantity
        
    def __str__(self):
        return self.product
    
class OldCart(models.Model):
    user            = models.ForeignKey(Account, on_delete=models.CASCADE ,null =True)
    product         = models.ForeignKey(Products, on_delete = models.CASCADE)
    Quantity        = models.IntegerField()
    date_added      = models.DateField(auto_now_add = True ,null = True)
    
    def __str__(self):
        return self.user