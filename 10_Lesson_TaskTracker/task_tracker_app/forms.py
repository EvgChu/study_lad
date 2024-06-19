from django import forms
from .models import Task, Comment, Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name', 
            'description', 
            'start_date', 
            'due_date', 
            'status', 
            'manager',
            'members'
            ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(choices=Project.Status),
            'members': forms.ModelMultipleChoiceField()
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'name', 
            'description', 
            # 'project', будет назначатся автоматически ??
            # 'creator', 
            'assigned_to', 
            'priority', 
            'due_date', 
            'status'
        ]

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
