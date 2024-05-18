from django.urls import path, register_converter
from. import views, converters


register_converter(converters.FourDigitConverter, 'yyyy')

urlpatterns = [
    path('', views.index, name='index'),
    path('<yyyy:year>', views.index, name='year'),
    path('type/', views.get_show_types, name='types'),
    path('type/<type_sign>', views.get_info_about_type, name='horoscope_types'),
    path('<int:month>/<int:day>', views.get_info_about_day, name='day'),
    path('<int:sign_horoscope>/', views.get_info_about_sign_zodiac_by_number, name='zodiac_by_number'),
    path('<sign_horoscope>/', views.get_info_about_sign_zodiac, name='horoscope_name'),
]
