from django.shortcuts import render
from django.http import HttpResponse

from .forms import UserForm

def index(request):
    userform = UserForm()
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            return HttpResponse(f'{userform.cleaned_data["name"]} {userform.cleaned_data["age"]}')
    return render(request, 'first/index.html', {"form": userform})