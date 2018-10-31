from django.urls import path,include

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('view', views.vew, name = 'view'),  
    path('approval', views.approval, name = 'approval'),
    path('removal', views.removal, name = 'removal'),
    path('modify', views.modify, name = 'modify'),
]

