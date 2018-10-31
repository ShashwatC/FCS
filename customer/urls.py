from django.urls import path,include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
<<<<<<< HEAD
    path('account/',views.account, name='account'),
    path('account/deposit/',views.deposit, name='deposit'),
    path('account/withdraw/',views.withdraw, name='deposit'),
    path('account/transfer/',views.transfer, name='deposit')
=======
    path('account',views.account, name='account'),
    path('create',views.create_acc, name='create'),
    path('edit_prof',views.edit_prof, name='edit_prof'),
>>>>>>> ea92b1a00b077a027c2a9fd6a0b991e4fe74f589
]

