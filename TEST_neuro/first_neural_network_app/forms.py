from django import forms
from .models import NeuroNet, Layer

class NeuroNetForm(forms.ModelForm):
    class Meta:
        model = NeuroNet
        fields = ['name', 'first_layer', 'number_of_layers']

class LayerForm(forms.ModelForm):
    class Meta:
        model = Layer
        fields = ['name', 'size', 'next_layer', 'alpha', 'type_fn_activation']

