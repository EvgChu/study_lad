from django import forms

class UserForm(forms.Form):
    name = forms.CharField(
        label="Имя", 
        widget=forms.Textarea,
        initial="Дядя Ваня",
        help_text="Введите имя",
    )
    age = forms.IntegerField(
        label="Возраст",
        initial=18,
        help_text="Введите возраст",
    )
    field_order = ['age', 'name']
