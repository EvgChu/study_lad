from django.db import models
from django.utils import timezone
# Create your models here.


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DR",  'DRAFT'
        PUBLISHED = "PB", 'PUBLISHED'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, unique_for_date='publish')
    author  = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')

    body  = models.TextField()

    publish = models.DateTimeField(default=timezone.now)
    created  = models.DateTimeField(auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True)
    status  = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)


    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse(
            "blog:post_datail", 
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day, 
                self.slug
            ]
        )
    
    class Meta:
        ordering = ['-publish']
        index = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
    