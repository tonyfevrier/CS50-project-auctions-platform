from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from auctions.models import Listing, Bid, Comment 

from .models import User


def index(request):
    listings = Listing.objects.filter(winner="")
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
        Listing.objects.create(title = request.POST['title'],
                                description = request.POST['description'],
                                price = request.POST["price"],
                                url = request.POST["url"],
                                category = request.POST["category"],
                                creator = request.user)  
        return HttpResponseRedirect(f'/listing/{Listing.objects.last().id}')
    return render(request,"auctions/newlisting.html")


def categories(request):
    """
    View rendering a template listing all the categories registered by listings creator
    """
    categories = set(listing.category for listing in Listing.objects.all())
    categories.remove("")
    return render(request, "auctions/categories.html", context={'categories':categories})


def listing(request, id):
    """
    View rendering the listing associated with the listing id 
    """  
    listing = Listing.objects.get(id = id) 
    useriscreator = (request.user == listing.creator) 
    userisfollower = (request.user.username in listing.followers)
    useriswinner = (request.user.username == listing.winner)
    return render(request,"auctions/listing.html", context={"listing":listing,
                                                            "bid":Bid.objects.filter(listing=listing).last(),
                                                            "bidnumber":len(Bid.objects.filter(listing=listing)),
                                                            "useriscreator":useriscreator,
                                                            "userisfollower":userisfollower,
                                                            "useriswinner":useriswinner,
                                                            "comments":reversed(Comment.objects.filter(listing=listing))})


def category_listings(request,category):
    """
    View rendering all listings of a given category
    """
    listings = Listing.objects.filter(category=category, winner="")
    return render(request, "auctions/category_listings.html", context={'category':category, 
                                                                       'listings':listings})


@login_required
def watchlist(request):
    """
    View rendering the watchlist of a user
    """ 
    watchlistings = []
    for listing in Listing.objects.filter(winner=""):
        if request.user.username in listing.followers:
            watchlistings.append(listing)
    return render(request,"auctions/watchlist.html",context={'watchlistings':watchlistings})


@login_required
def toggletowatchlist(request,id):
    """
    View to add a user to the watchlist
    """
    listing = Listing.objects.get(id=id) 
    if request.user.username in listing.followers:
        listing.followers.remove(request.user.username)
    else:
        listing.followers.append(request.user.username)
    listing.save()
    return HttpResponseRedirect(f'/listing/{id}')


@login_required
def submitbid(request,id):
    """
    View launched when a user submit a bid
    """     
    price = request.POST["bid"]
    listing = Listing.objects.get(id=id)
    lastbid = Bid.objects.filter(listing=listing).last()
    if lastbid is not None:
        lastprice = lastbid.price   
    else:
        lastprice = listing.price
    useriscreator = (request.user == listing.creator) 
    userisfollower = (request.user.username in listing.followers)

    if float(price) <= lastprice: 
        message = "You have to write a price superior to the actual price"
        return render(request, "auctions/listing.html", context={"listing":listing,
                                                                 "bid":lastbid,
                                                                 'message':message,
                                                                 'bidnumber':len(Bid.objects.filter(listing=listing)),
                                                                 'useriscreator':useriscreator,
                                                                 'userisfollower':userisfollower,
                                                                 "comments":reversed(Comment.objects.filter(listing=listing))})
    else: 
        bid = Bid.objects.create(price=price, listing=listing, bidder=request.user)
        return render(request, "auctions/listing.html", context={"listing":listing,
                                                                 'bid':bid,
                                                                 'bidnumber':len(Bid.objects.filter(listing=listing)),
                                                                 'useriscreator':useriscreator,
                                                                 'userisfollower':userisfollower,
                                                                 "comments":reversed(Comment.objects.filter(listing=listing))})



@login_required
def deletelisting(request, id):
    """
    View deleting a given listing.
    """
    listing = Listing.objects.get(id=id)
    listing.winner = request.user.username
    listing.save()
    return HttpResponseRedirect('/')


@login_required
def savecomment(request, id):
    """
    View saving the comments
    """
    Comment.objects.create(text=request.POST['text'], writer=request.user, listing=Listing.objects.get(id=id))
    return HttpResponseRedirect(f'/listing/{id}') 