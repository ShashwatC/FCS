from django.contrib import admin
from bank.models import Account
<<<<<<< HEAD
=======
from .models import Trans


admin.site.register(Account)
admin.site.register(Trans)
>>>>>>> ea92b1a00b077a027c2a9fd6a0b991e4fe74f589

admin.site.register(Account)
# Register your models here.
