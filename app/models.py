from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Userregister(AbstractUser):
    phone_number = models.IntegerField(null=True,blank=True)
    account_number = models.IntegerField(null=True,blank=True)
    minimum_balance = models.IntegerField(null=True,blank=True)
    adhar_number = models.IntegerField(null=True,blank=True)
    pan_card = models.IntegerField(null=True,blank=True)
    pin = models.IntegerField(null=True,blank=True)
    user_type = models.CharField(max_length=50)
    bankname = models.CharField(max_length=50)
    IFSC = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)
    image = models.FileField()

class History(models.Model):
    user_id = models.IntegerField()
    details = models.CharField(max_length=50)
    date = models.DateField(auto_now=True)
    history_amount = models.IntegerField()





    def __str__(self):
        return self.username