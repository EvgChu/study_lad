from django import forms

from .models import Person

class PersonForm(forms.ModelForm):
    name = forms.CharField(label="Имя")
    age = forms.IntegerField(label="Возраст")

    class Meta:
        model = Person
        fields = ['name', 'age']
