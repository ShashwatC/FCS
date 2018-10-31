from django.urls import path,include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('account/',views.account, name='account'),
    path('account/deposit/',views.deposit, name='deposit'),
    path('account/withdraw/',views.withdraw, name='deposit'),
    path('account/transfer/',views.transfer, name='deposit')
]

