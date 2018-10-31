from django.contrib import admin
from bank.models import Account
from .models import Trans


admin.site.register(Account)
admin.site.register(Trans)
# Register your models here.
