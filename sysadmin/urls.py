from django.urls import path,include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pending', views.pending, name='pending requests'),
    path('removal', views.del_internal, name='del_internal'),
    path('view', views.view_trans, name='view_trans'),
    path('approv', views.acc_pen, name='approv'),
    
]

