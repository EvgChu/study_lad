from django.urls import path 

from . import views

urlpatterns = [
    path('<int:rubric_id>/', views.rubric_bbs, name='rubric'),
    path('', views.index, name='index'),
]
