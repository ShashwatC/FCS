from django.urls import path,include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('account/',views.account, name='account'),
    path('account/deposit/',views.deposit, name='deposit'),
    path('account/withdraw/',views.withdraw, name='deposit'),
    path('account/transfer/',views.transfer, name='deposit'),
    path('create',views.create_acc, name='create'),
    path('edit_prof',views.edit_prof, name='edit_prof'),
]

