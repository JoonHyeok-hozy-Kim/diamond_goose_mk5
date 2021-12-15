from django.db import models

# Create your models here.


class Laboratory(models.Model):

    creation_date = models.DateTimeField(auto_now=True)