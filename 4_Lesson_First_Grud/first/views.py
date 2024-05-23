from django.shortcuts import render
from django.http import HttpResponse

from .forms import UserForm

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        return HttpResponse(name + ' ' + age)
    userform = UserForm()
    return render(request, 'first/index.html', {"form": userform})