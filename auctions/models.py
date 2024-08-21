from django.contrib.auth.models import AbstractUser
from django.db import models 

from datetime import datetime



class User(AbstractUser):
    pass


class Listings(models.Model):
    title = models.TextField(default="")
    description = models.TextField(default="") 
    price = models.FloatField(default=0.)
    url = models.URLField(default="",null=True,blank=True)
    category = models.TextField(default="",null=True,blank=True)
    created_at = models.DateTimeField(default=datetime.now) 

