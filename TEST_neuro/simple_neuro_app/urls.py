
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('neuron/add/', views.add_neuron, name='add_neuron'),
    path('neuron/<int:pk>/', views.calculate, name='calculate'),
    path('neuron/<int:pk>/edit/', views.neuron_edit, name='neuron_edit'),
]
