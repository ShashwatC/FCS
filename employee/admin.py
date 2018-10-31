from django.contrib import admin
from bank.models import Profile,Transaction,Account

admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Profile)
# Register your models here.
