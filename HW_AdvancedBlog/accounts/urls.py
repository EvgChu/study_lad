from . import views
from django.urls import path
from django.urls import re_path

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signin/', views.signin, name='user'),
]