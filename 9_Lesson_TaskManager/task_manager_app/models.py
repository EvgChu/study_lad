from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'АКТ', 'Активная'
        DONE = 'ЗВР', 'Завершённая'

    class Priority(models.TextChoices):
        low = 'Низкая'
        medium = 'Средняя'
        high = 'Высокая'

    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField(null=True, blank=True, default=None)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.medium)  
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-due_date',)
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Comment(models.Model):
    creator  = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    task  = models.ForeignKey(Task, on_delete=models.CASCADE)
    text  = models.TextField()
    created   = models.DateTimeField(auto_now_add=True)

