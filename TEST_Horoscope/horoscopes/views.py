from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

# Create your views here.

zodiac_dict = {
    'aries': 'Овен - первый знак зодиака, планета Марс (с 21 марта по 20 апреля).',
    'taurus': 'Телец - второй знак зодиака, планета Венера (с 21 апреля по 21 мая).',
    'gemini': 'Близнецы - третий знак зодиака, планета Меркурий (с 22 мая по 21 июня).',
    'cancer': 'Рак - четвёртый знак зодиака, Луна (с 22 июня по 22 июля).',
    'leo': ' Лев - <i>пятый знак зодиака</i>, солнце (с 23 июля по 21 августа).',
    'virgo': 'Дева - шестой знак зодиака, планета Меркурий (с 22 августа по 23 сентября).',
    'libra': 'Весы - седьмой знак зодиака, планета Венера (с 24 сентября по 23 октября).',
    'scorpio': 'Скорпион - восьмой знак зодиака, планета Марс (с 24 октября по 22 ноября).',
    'sagittarius': 'Стрелец - девятый знак зодиака, планета Юпитер (с 23 ноября по 22 декабря).',
    'capricorn': 'Козерог - десятый знак зодиака, планета Сатурн (с 23 декабря по 20 января).',
    'aquarius': 'Водолей - одиннадцатый знак зодиака, планеты Уран и Сатурн (с 21 января по 19 февраля).',
    'pisces': 'Рыбы - двенадцатый знак зодиака, планеты Юпитер (с 20 февраля по 20 марта).',
}


def get_info_about_sign_zodiac(request, sign_horoscope):
    description = zodiac_dict.get(sign_horoscope, None)

    if description is None:
        return HttpResponseNotFound(f'Знак зодиака {sign_horoscope} не найден')
    else:
        return HttpResponse(description)


def get_info_about_sign_zodiac_by_number(request, sign_horoscope):
    zodiac = list(zodiac_dict.keys())

    if sign_horoscope > len(zodiac) or sign_horoscope < 1:
        return HttpResponseNotFound(f'Знак зодиака {sign_horoscope} не найден')
    else:
        redirect_url = reverse("horoscope_name", args=[zodiac[sign_horoscope - 1]])
        return HttpResponseRedirect(redirect_url)
                