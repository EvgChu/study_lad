from django.shortcuts import render
from django.http import HttpResponse

from .models import Bb
# Create your views here.

def index(request):
    res = ''
    for bb in Bb.objects.order_by('-published'):
        res += bb.title + ': ' + bb.content + '<br>'
    return HttpResponse(res)