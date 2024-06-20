
from django.urls import path
from . import views

urlpatterns = [
    path('', views.neuronet_list, name='neuronet_list'),
    path('create_neuronet/', views.create_neuronet, name='create_neuronet'),
    path('add_layer/<int:neuronet_id>/', views.add_layer, name='add_layer'),
    path('train_neuronet/<int:neuronet_id>/', views.train_neuronet, name='train_neuronet'),
]

