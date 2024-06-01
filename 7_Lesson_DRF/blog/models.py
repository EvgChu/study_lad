from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey()

    def __str__(self) -> str:
        return f"{self.title}"

class Category(models.Model):
    name = models.CharField(max_length=100, index=True)

    def __str__(self) -> str:
        return f"{self.name}"