from django import forms

class EmailPostForm(forms.Form):
    email = forms.EmailField(label='Email')
    name = forms.CharField(label='Name', required=False)
