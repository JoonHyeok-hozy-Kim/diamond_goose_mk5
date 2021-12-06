from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from articleapp.models import Article


class Comment(models.Model):
    owner = models.ForeignKey(User,on_delete=models.SET_NULL, related_name='comment', null=True)
    article = models.ForeignKey(Article,on_delete=models.SET_NULL, related_name='comment', null=True)

    content = models.TextField(null=False)
    creation_date = models.DateTimeField(auto_now=True)