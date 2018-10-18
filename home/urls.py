from django.urls import path,include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login_success',views.login_success,name='login_success'),
    path('accounts/register/',views.register,name='register'),
    path('accounts/more/',views.registration_details,name='register_more'),
]

