from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


# Create your models here.

class Post(models.Model):
    STATUS_CHOICES = (

        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=200)
    body = models.TextField()
    slug = models.SlugField(max_length=100,unique_for_date='publish' )
    image = models.ImageField(upload_to='blog_pics/%Y/%m/%d', blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now=True)
    updated= models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="draft")


    class Meta:
        ordering = ('-publish',)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.slug, self.publish.year, self.publish.month, self.publish.day])
    
