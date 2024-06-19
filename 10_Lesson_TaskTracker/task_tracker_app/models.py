from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    class Status(models.TextChoices):
        NEW = 'Новая'
        IN_PROGRESS = 'В процессе'
        DONE = 'Завершённая'

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    manager = models.ForeignKey(User, related_name='managed_projects', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='projects')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)

    start_date = models.DateTimeField()
    due_date = models.DateField()
    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Task(models.Model):
    class Status(models.TextChoices):
        NEW = 'Новая'
        IN_PROGRESS = 'В процессе'
        IN_TESTING = 'В тестировании'
        DONE = 'Завершённая'

    class Priority(models.TextChoices):
        low = 'Низкая'
        medium = 'Средняя'
        high = 'Высокая'

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name='created_tasks', null=True, blank=True, on_delete=models.SET_NULL)
    assigned_to = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.CASCADE)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.medium)  
    due_date = models.DateField()
    end_date   = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    text  = models.TextField()
    creator = models.ForeignKey(User, related_name='comments', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
