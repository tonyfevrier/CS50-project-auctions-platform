from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from auctions.models import Listings 

from .models import User


def index(request):
    listings = Listings.objects.all()
    return render(request, "auctions/index.html",context={'listings':listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def newlisting(request):
    """
    View rendering the page to create a new listing
    """
    if request.method == "POST":
        Listings.objects.create(title = request.POST['title'],
                                description = request.POST['description'],
                                price = request.POST["price"],
                                url = request.POST["url"],
                                category = request.POST["category"]) 
    return render(request,"auctions/newlisting.html")


def listing(request, id):
    """
    View rendering the listing associated with the listing id 
    """  
    listing = Listings.objects.get(id = id) 
    return render(request,"auctions/listing.html", context={"listing":listing})


def watchlist(request):
    """
    View rendering the watchlist of a user
    """
    return render(request,"auctions/watchlist.html")


def addtowatchlist(request,id):
    """
    View to add a user to the watchlist
    """
    listing = Listings.objects.get(id=id)
    listing.followed = True
    listing.save()
    return HttpResponseRedirect('')