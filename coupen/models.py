from django.db import models
from django.core.validators import MinValueValidator, MaxLengthValidator
# Create your models here.



class Coupens(models.Model):
    coupen_code        = models.CharField(max_length=200)
    coupen_limit       = models.IntegerField()
    validity_upto      = models.DateField()
    is_used            = models.BooleanField(null=True , blank=True , default=False)
    discount           = models.IntegerField(validators=[MinValueValidator(0),MaxLengthValidator(100)])
    is_active          = models.BooleanField(default=True)