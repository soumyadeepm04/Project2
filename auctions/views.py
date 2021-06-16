from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Bid, User, AuctionListings, Watchlist

from django.contrib.auth.decorators import login_required


def index(request):
    if AuctionListings.objects.exists():
        return render(request, "auctions/index1.html", {
            "auction_listings":AuctionListings.objects.all()
        })
    
    else:
        return render(request, "auctions/index.html")


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
def create_listings(request):
    if request.method == "POST":
        if request.POST["url"] != None or "":
            AuctionListings.objects.create(title = request.POST["title"], description = request.POST["description"], starting_bid = request.POST["starting_bid"], urls = request.POST["url"], price = request.POST["starting_bid"], user = request.user, open = "open")
        else:
            AuctionListings.objects.create(title = request.POST["title"], description = request.POST["description"], starting_bid = request.POST["starting_bid"], price = request.POST["starting_bid"], user = request.user, open = "open")

        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "auctions/create_listings.html")

@login_required
def listing_details(request, listing_id):
    item_details = AuctionListings.objects.get(id = listing_id)
    if AuctionListings.objects.get(id = listing_id).open == "open":
        if request.user == AuctionListings.objects.get(pk = listing_id).user:
            return render(request, "auctions/listing_details+closing.html", {
                "item":item_details, "listing_id":listing_id
            })
        else:
            return render(request, "auctions/listing_details.html", {
                "item":item_details, "listing_id":listing_id
            })
    
    else:
        a = AuctionListings.objects.get(id = listing_id).price
        b = Bid.objects.get(bid = a)
        if request.user == b.user:
            return render(request, "auctions/close_listing_win.html")
        else:
            return render(request, "auctions/close_listing.html",{
                "item":item_details, "listing_id":listing_id
            })

@login_required
def add_watchlist(request, listing_id):
    if request.method == "POST":
        if Watchlist.objects.filter(item = listing_id).exists():
            return render(request, "auctions/watchlist_exists.html")
        else:
            auction_listing = AuctionListings.objects.get(pk = listing_id)
            current_user = request.user
            Watchlist.objects.create(user = current_user, item = auction_listing)
            return HttpResponseRedirect(reverse("watchlist"))

@login_required
def watchlist(request):
    a = Watchlist.objects.filter(user = request.user).values_list('item')
    watchlist_items = []
    for x in a:
        watchlist_items.append(AuctionListings.objects.get(pk = x[0]))
    return render(request, "auctions/watchlist.html", {
        "watchlist_items":watchlist_items, "Watchlist":Watchlist()
    })

@login_required
def remove_watchlist(request, listing_id):
    Watchlist.objects.get(item = listing_id).delete()
    return HttpResponseRedirect(reverse("watchlist"))

@login_required
def bid(request, listing_id):
    if request.method == "POST":
        if int(request.POST["bid"]) <= AuctionListings.objects.get(pk = listing_id).price:
            return render(request, "auctions/invalid_bid.html")
        else:
            Bid.objects.create(user = request.user, bid = request.POST["bid"])
            t = AuctionListings.objects.get(id = listing_id)
            t.price = request.POST["bid"]
            t.save(update_fields = ['price'])
            return HttpResponseRedirect(reverse("watchlist"))

def close_listing(request, listing_id):
    t = AuctionListings.objects.get(pk = listing_id)
    t.open = "closed"
    t.save(update_fields = ['open'])
    return HttpResponseRedirect(reverse("index"))
