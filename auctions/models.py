from django.contrib.auth.models import AbstractUser
from django.db import models 

from django.utils import timezone



class User(AbstractUser):
    pass


class Listings(models.Model):
    title = models.CharField(default="", max_length=100)
    description = models.TextField(default="") 
    price = models.FloatField(default=0.)
    url = models.URLField(default="", null=True, blank=True)
    category = models.CharField(default="", null=True, blank=True, max_length=50)
    created_at = models.DateTimeField(default=timezone.now)  
    followers = models.JSONField(default=[])
    creator = models.CharField(default="", max_length=50)
    winner = models.CharField(default="", max_length=50)


class Bids(models.Model):
    price = models.FloatField(default=0.)
    listing = models.ForeignKey(Listings,on_delete=models.CASCADE)
    bidder = models.CharField(default="",max_length=50)


class Comments(models.Model):
    text = models.TextField(default="")
    writer = models.CharField(default="", max_length=50)
    listing = models.ForeignKey(Listings,on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)  



