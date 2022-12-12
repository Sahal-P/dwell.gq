from django.db import models
from accounts.models import Account
# Create your models here.


class Wallet(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.FloatField(null=False, default=0)
    added_at = models.DateTimeField(auto_now_add=True)
    

