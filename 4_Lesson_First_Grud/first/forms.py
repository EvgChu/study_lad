from django import forms

class UserForm(forms.Form):
    name = forms.CharField(
        label="Имя", 
        widget=forms.Textarea,
        initial="Дядя Ваня",
        help_text="Введите имя",
        max_length=10,
        min_length=2,
    )
    age = forms.IntegerField(
        label="Возраст",
        initial=18,
        help_text="Введите возраст",
        max_value=100,
        min_value=18,
    )
    ads = forms.BooleanField(label="Подтвердите", required=False)
