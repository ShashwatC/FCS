from django.urls import path,include

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('view', views.vew, name = 'view'),  
    path('approval', views.approval, name = 'approval'),
    path('removal', views.removal, name = 'removal'),
    path('modify', views.modify, name = 'modify'),
    path('account_pending', views.acc_pen, name = 'acc_pen'),
    path('withdraw', views.withdraw, name = 'withdraw'),
    path('deposit', views.deposit, name = 'deposit'),
    path('modify', views.deposit, name = 'deposit'),
    


    
]

