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
    pending = models.BooleanField(default=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15)
    private_key = models.CharField(max_length=512)


class Logs(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=256)


class Transaction(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    sender = models.ForeignKey(User, on_delete="PROTECT", related_name="sender")
    sender_acc = models.ForeignKey(Account, on_delete="PROTECT", related_name="sender_acc")
    receiver = models.ForeignKey(User, on_delete="PROTECT", related_name="receiver")
    receiver_acc = models.ForeignKey(Account, on_delete="PROTECT", related_name="receiver_acc")
    amount = models.PositiveIntegerField()
    pending = models.BooleanField(default=True)

class Deposit(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete="PROTECT", related_name="owner_d")
    owner_acc = models.ForeignKey(Account, on_delete="PROTECT", related_name="owner_acc_d")
    amount = models.PositiveIntegerField()
    pending = models.BooleanField(default=True)

class Withdraw(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete="PROTECT", related_name="owner_w")
    owner_acc = models.ForeignKey(Account, on_delete="PROTECT", related_name="owner_acc_w")
    amount = models.PositiveIntegerField()
    pending = models.BooleanField(default=True)


class Pending(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField()
    choice = models.IntegerField()
    mobile_number = models.CharField(max_length=100)


class Access(models.Model):
    owner = models.ForeignKey(User, on_delete="PROTECT", related_name="is_owner")
    acc_num = models.ForeignKey(Account, on_delete="PROTECT")
    access_req = models.ForeignKey(User, on_delete="PROTECT", related_name="wants_access")
