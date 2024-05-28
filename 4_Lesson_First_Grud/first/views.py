from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

from .forms import UserForm
from .models import Person

# def index(request):
#     userform = UserForm()
#     if request.method == 'POST':
#         userform = UserForm(request.POST)
#         if userform.is_valid():
#             return HttpResponse(f'{userform.cleaned_data["name"]} {userform.cleaned_data["age"]}')
#     return render(request, 'first/index.html', {"form": userform})


def index(request):
    people = Person.objects.all()
    return render(request, 'first/index.html', {"people":people})


def create(request):
    if request.method == 'POST':
        person = Person(name=request.POST['name'], age=request.POST['age'])
        person.save()


    return HttpResponseRedirect('/')

def edit(request, id):
    try:
        person  = Person.objects.get(id=id)
        if request.method  ==  'POST':
            person.name = request.POST['name']
            person.age = request.POST['age']
            person.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'first/edit.html', {'person': person})
    except Person.DoesNotExist:
        return HttpResponseNotFound('Not found')

def delete(request, id):
    try:
        person = Person.objects.get(id=id)
        person.delete()
        return HttpResponseRedirect('/')
    except Person.DoesNotExist:
        return HttpResponseNotFound('Not found')
