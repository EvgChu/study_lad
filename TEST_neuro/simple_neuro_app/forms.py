from django import forms
from .models import Neuron

class NeuronForm(forms.ModelForm):
    class Meta:
        model = Neuron
        fields = '__all__'

class InputDataFrom(forms.Form):
    input_data = forms.CharField(widget=forms.Textarea(attrs={'rows': '2', 'cols': '20'}))