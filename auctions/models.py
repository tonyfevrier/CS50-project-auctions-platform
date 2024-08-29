from django.contrib.auth.models import AbstractUser
from django.db import models 
from django.utils import timezone

from commerce import settings



class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(default="", max_length=100)
    description = models.TextField(default="") 
    price = models.FloatField(default=0.)
    url = models.URLField(default="", blank=True)
    category = models.CharField(default="", blank=True, max_length=50)
    created_at = models.DateTimeField(default=timezone.now)  
    followers = models.JSONField(default=[], blank=True) 
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    winner = models.CharField(default="", max_length=50, blank=True)


class Bid(models.Model):
    price = models.FloatField(default=0.)
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE)
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)


class Comment(models.Model):
    text = models.TextField(default="")
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)  



