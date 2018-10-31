from django.db import models
from django.contrib.auth.models import User, AbstractUser
import uuid


# Create your models here.


class Account(models.Model):
    # id is internal unique ID, acc_num is external
    id = models.AutoField(primary_key=True)
    acc_num = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    owner = models.ForeignKey(User, on_delete="PROTECT")
    balance = models.FloatField()


class Profile(models.Model):
    mobile_number = models.CharField(max_length=15)
    private_key = models.CharField(max_length=512)


class Logs(models.Model):
    timestamp = models.DateTimeField()
    message = models.CharField(max_length=256)


class Transaction(models.Model):
    timestamp = models.DateTimeField()
    sender = models.ForeignKey(User, on_delete="PROTECT", related_name="sender")
    receiver = models.ForeignKey(User, on_delete="PROTECT", related_name="receiver")
    amount = models.PositiveIntegerField()
    pending = models.BooleanField(default=True)


class Pending(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField()
    choice = models.IntegerField()
    mobile_number = models.CharField(max_length=100)