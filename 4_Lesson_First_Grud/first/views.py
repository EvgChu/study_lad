from django.shortcuts import render
from django.http import HttpResponse

from .forms import UserForm

def index(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            return HttpResponse(
                userform.changed_data['name'] + ' ' + userform.changed_data['name']
            )
        else:
            return HttpResponse('Invalid form')
    userform = UserForm()
    return render(request, 'first/index.html', {"form": userform})