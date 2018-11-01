from django.urls import path,include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('account/',views.account, name='account'),
    path('account/deposit/',views.deposit, name='deposit'),
    path('account/withdraw/',views.withdraw, name='withdraw'),
    path('account/transfer/',views.transfer, name='transfer'),
    path('transfer_pend',views.transfer_comp, name='transfer_pend'),
    path('deposit_comp',views.deposit_comp, name='deposit_comp'),
    path('withdraw_comp',views.withdraw_comp, name='withdraw_comp'),
    path('create',views.create_acc, name='create'),
    path('edit_prof',views.edit_prof, name='edit_prof'),
]

