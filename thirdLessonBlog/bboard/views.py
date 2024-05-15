from django.shortcuts import render
from django.http import HttpResponse

from .models import Bb
# Create your views here.

def index(request):
    bbs = Bb.objects.all()

    return render(request, 'bboard/index.html', {'bbs': bbs})