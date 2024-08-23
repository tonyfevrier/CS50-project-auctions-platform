from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from auctions.models import Listings, Bids 

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
        
        Bids.objects.create(price = request.POST["price"],
                            listing = Listings.objects.last())
    return render(request,"auctions/newlisting.html")


def listing(request, id):
    """
    View rendering the listing associated with the listing id 
    """  
    listing = Listings.objects.get(id = id) 
    return render(request,"auctions/listing.html", context={"listing":listing,
                                                            "bid":Bids.objects.filter(listing=listing).last(),
                                                            "bidnumber":len(Bids.objects.filter(listing=listing))})


@login_required
def watchlist(request):
    """
    View rendering the watchlist of a user
    """
    watchlistings = Listings.objects.filter(followed = True)
    return render(request,"auctions/watchlist.html",context={'watchlistings':watchlistings})


def toggletowatchlist(request,id):
    """
    View to add a user to the watchlist
    """
    listing = Listings.objects.get(id=id)
    listing.followed = not listing.followed
    listing.save()
    return HttpResponseRedirect(f'/listing/{id}')


@login_required
def submitbid(request,id):
    """
    View launched when a user submit a bid
    """    
    price = request.POST["bid"]
    listing = Listings.objects.get(id=id)
    lastbid = Bids.objects.filter(listing=listing).last() 
    if float(price) <= lastbid.price: 
        message = "You have to write a price superior to the actual price"
        return render(request, "auctions/listing.html", context={"listing":listing,
                                                                 "bid":lastbid,
                                                                 'message':message,
                                                                 'bidnumber':len(Bids.objects.filter(listing=listing))})
    else: 
        bid = Bids.objects.create(price=price,listing=listing)
        return render(request, "auctions/listing.html", context={"listing":listing,
                                                                 'bid':bid,
                                                                 'bidnumber':len(Bids.objects.filter(listing=listing))})
