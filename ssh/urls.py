from django.urls import path
from . import views

urlpatterns = [
    path('', views.home , name='ssh-home'),
    path('priv/', views.priv , name='ssh-priv'),
    path('config/', views.config , name='ssh-config'),
]