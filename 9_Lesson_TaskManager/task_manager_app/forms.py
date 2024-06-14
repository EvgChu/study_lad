from django import forms
from .models import Task, Comment

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'due_date',
            'status',
            'priority'
        ]
        labels = {
            'title': 'Название задачи',
            'description': 'Подробное описание',
            'due_date': 'Дата выполнения',
            'status': 'Текущий статус',
            'priority': 'Приоритет задачи'
        }
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(choices=Task.Status),
            'priority': forms.Select(choices=Task.Priority),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Комментарий'
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 50})
        }
