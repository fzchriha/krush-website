from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User


class Post(models.Model):
    name = models.CharField(max_length=250)
    nickname = models.TextField(default="misterieux")
    content = models.TextField()
    published = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100)
    tags = TaggableManager()

    def __str__(self):
        return self.name