from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Article(models.Model):
    owner = models.ForeignKey(User,on_delete=models.SET_NULL, related_name='article',null=True)

    title = models.CharField(max_length=200, null=False)
    image = models.ImageField(upload_to='articles/', null=False)
    content = models.TextField(null=True)

    creation_date = models.DateTimeField(auto_now=True)
    last_update_date = models.DateTimeField(auto_now_add=True)