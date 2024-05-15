from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login(request):
    return HttpResponse("login")

# Create your views here.
def signin(request):
    return HttpResponse("signin")