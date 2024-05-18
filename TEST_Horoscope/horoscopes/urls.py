from django.urls import path
from. import views

urlpatterns = [
    path('', views.index, name='index'),
    path('type/', views.get_show_types, name='types'),
    path('type/<type_sign>', views.get_info_about_type, name='horoscope_types'),
    path('<int:sign_horoscope>/', views.get_info_about_sign_zodiac_by_number, name='zodiac_by_number'),
    path('<sign_horoscope>/', views.get_info_about_sign_zodiac, name='horoscope_name'),
]
