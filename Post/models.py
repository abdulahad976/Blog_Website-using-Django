from django.db import models
from django.utils import timezone


class Post(models.Model):
    DRAFT = 'D'
    PUBLISHED = 'P'
    ARCHIVED = 'A'

    Status = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
        (ARCHIVED, 'Archived'),
    ]
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=200)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status, default=DRAFT)

    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish']),]


    def __str__(self):

        return self.title

