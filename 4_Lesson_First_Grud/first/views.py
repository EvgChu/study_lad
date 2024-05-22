from django.shortcuts import render

from .forms import UserForm

def index(request):
    form = UserForm()
    return render(request, 'first/index.html', {"form": form})