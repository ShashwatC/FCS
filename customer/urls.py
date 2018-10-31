from django.urls import path,include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('account',views.account, name='account'),
    path('create',views.create_acc, name='create'),
    path('edit_prof',views.edit_prof, name='edit_prof'),
]

