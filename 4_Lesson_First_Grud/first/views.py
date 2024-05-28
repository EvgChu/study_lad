from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.forms.models import model_to_dict


from .forms import PersonForm
from .models import Person

# def index(request):
#     userform = UserForm()
#     if request.method == 'POST':
#         userform = UserForm(request.POST)
#         if userform.is_valid():
#             return HttpResponse(f'{userform.cleaned_data["name"]} {userform.cleaned_data["age"]}')
#     return render(request, 'first/index.html', {"form": userform})


def index(request):
    form = PersonForm()
    people = Person.objects.all()
    return render(request, 'first/index.html', {"form": form, "people": people})


def create(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect('/')


def edit(request, id):
    try:
        person  = Person.objects.get(id=id)
        if request.method  ==  'POST':
            form = PersonForm(request.POST, instance=person)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect('/')
        else:
            form = PersonForm(instance=person)
            return render(request, 'first/edit.html', {'form': form})
    except Person.DoesNotExist:
        return HttpResponseNotFound('Not found')

def delete(request, id):
    try:
        person = Person.objects.get(id=id)
        person.delete()
        return HttpResponseRedirect('/')
    except Person.DoesNotExist:
        return HttpResponseNotFound('Not found')
