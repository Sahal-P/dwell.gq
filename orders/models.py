from django.db import models
from accounts.models import Account,Address
from cart.models import CartItem
from category.models import Products
# Create your models here.



class Orders(models.Model):
    product         = models.ForeignKey(Products, on_delete= models.SET_NULL,null=True)
    user            = models.ForeignKey(Account, on_delete= models.SET_NULL, null=True)
    address         = models.TextField(null=True)
    total_price     = models.FloatField(null =False)
    grand_price     = models.FloatField(null = True , blank=True)
    offered_price   = models.FloatField(null = True , blank=True)
    coupen_applied  = models.CharField(null = True , blank=True, max_length=200)
    price           = models.FloatField(default =0,null =False)
    quantity        = models.IntegerField(default =0,null =False)
    payment         = models.CharField(max_length=100, default='cod')
    orderd_date     = models.DateTimeField(auto_now_add=True)
    status          = models.CharField(max_length=50, default='Pending')
    order_id        = models.CharField(max_length=500, null=True)
    variation_id    = models.CharField(max_length=500, null=True,default=0)
    payment_id      = models.CharField(max_length=500, null=True, blank=True)
    expected_date   = models.DateTimeField(null = True)
    delivered_date  = models.DateTimeField(null=True)

    def sub_total(self):
        return self.product.selling_price *self.quantity
    
    def name(self):
        a = Products.objects.get(id =self.product)
        return a.product_name