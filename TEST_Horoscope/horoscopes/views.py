from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

from django.shortcuts import render

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

sign_types = {
    'fire': ['aries', 'leo', 'sagittarius'],
    'earth': ['taurus', 'virgo', 'capricorn'],
    'air': ['gemini', 'libra', 'aquarius'],
    'water': ['cancer', 'scorpio', 'pisces']
}

zodiac_dates = {
    1:  {'capricorn': (1, 20),   'aquarius': (21, 31)},
    2:  {'aquarius': (1, 19),    'pisces': (20, 29)},
    3:  {'pisces': (1, 20),      'aries': (21, 31)},
    4:  {'aries': (1, 20),       'taurus': (21, 30)},
    5:  {'taurus': (1, 21),      'gemini': (22, 31)},
    6:  {'gemini':  (1, 21),     'cancer': (22, 30)},
    7:  {'cancer':  (1, 22),     'leo': (23, 31)},
    8:  {'leo': (1, 21),         'virgo': (22, 31)},
    9:  {'virgo': (1, 22),       'libra': (23, 30)},
    10: {'libra': (1, 23),       'scorpio': (24, 31)},
    11: {'scorpio': (1, 22),     'sagittarius': (23, 30)},
    12: {'sagittarius': (1, 22), 'capricorn': (23, 31)}
}

def _create_lists(elemetns: list, viewname):
    li_elements = ""

    for sign in elemetns:
        li_elements += '<li><a href="{0}">{1}</a><br></li>'.format(reverse(viewname, args=[sign]), sign)
                
    result = f"<ol>{li_elements}</ol>"
    return result


def index(request, year=None):   
    return render(request, 'horoscopes/index.html', {"zodiacs": zodiac_dict.keys()})

                
def get_info_about_sign_zodiac(request, sign_horoscope):
    description = zodiac_dict.get(sign_horoscope.lower(), None)
    if description is None:
        return HttpResponseNotFound(f'Знак зодиака {sign_horoscope} не найден')
    else:
        return render(request, 'horoscopes/info_zodiac.html', {"description": description})


def get_info_about_sign_zodiac_by_number(request, sign_horoscope):
    zodiac = list(zodiac_dict.keys())

    if sign_horoscope > len(zodiac) or sign_horoscope < 1:
        return HttpResponseNotFound(f'Знак зодиака {sign_horoscope} не найден')
    else:
        redirect_url = reverse("horoscope_name", args=[zodiac[sign_horoscope - 1]])
        return HttpResponseRedirect(redirect_url)
    

def get_show_types(request):
    return HttpResponse(
        '<h1>Стихии зодиака</h1>'
        '<p>Выберите стихию зодиака:</p>'
        f'{_create_lists(sign_types.keys(), "horoscope_types")}'
    )

def get_info_about_type(request, type_sign):
    description = sign_types.get(type_sign.lower(), None)

    if description is None:
        return HttpResponseNotFound(f'Стихия зодиака {sign_types} не найден')
    else:
        return HttpResponse(
            f'<h1>Стихия {type_sign}</h1>'
            '<p>Выберите знак зодиака:</p>'
            f'{_create_lists(description, "horoscope_name")}'
        )


def get_info_about_day(request, month, day):

    if month in zodiac_dates:
        for sign in zodiac_dates[month]:
            if day >= zodiac_dates[month][sign][0] and day <= zodiac_dates[month][sign][1]:                  
                redirect_url = reverse(
                    "horoscope_name", 
                    args=[sign]
                )
                return HttpResponseRedirect(redirect_url)

    return HttpResponseNotFound(f'Знак зодиака {month} {day} не найден')
