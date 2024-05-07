from . import views
from django.urls import path
from django.urls import re_path

urlpatterns = [
    # re_path(r'^products/(?P<productId>\d+)', views.producut, name='producut'),
    # re_path(r'^products/$', views.producut, name='producut'),
    # re_path(r'^user/(?P<name>\w+)/(?P<id>\d+)', views.user, name='user'),
    path('products/<int:productId>/', views.producut, name='producut'),
    path('user/<str:name>/<int:id>/', views.user, name='user'),
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
]