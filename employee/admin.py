from django.contrib import admin
from bank.models import Account
from bank.models import Transaction


admin.site.register(Account)
admin.site.register(Transaction)
# Register your models here.
