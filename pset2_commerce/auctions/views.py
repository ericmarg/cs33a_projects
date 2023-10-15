from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import *


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.filter(is_active=True),
        "header": "Active Listings:"
    })


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


@login_required
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


# Renders an HTML page for the specific item the user clicked on
def get_listing(request, listing_id):
    return render(request, "auctions/listing.html", {
        "listing": Listings.objects.get(pk=listing_id),
        "bid_form": BidForm(),
        "comment_form": CommentForm(),
        "comments": Comments.objects.filter(listing_id=listing_id)
    })


# Renders page with a list of item categories to filter by
def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Listings.Categories
    })


# Allows users to bid on a listing. The bid must be greater than the current price of the listing.
@login_required
def bid(request, listing_id):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("index"))

    # POST path
    form = BidForm(request.POST)
    if form.is_valid():
        listing = Listings.objects.get(pk=listing_id)
        try:
            current_price = listing.highest_bid.amount
        # If no prior bid was made, highest_bid is None and has no amount attribute
        except AttributeError:  # No prior bid, so current price is list_price
            current_price = listing.list_price

        # Check bid amount is higher than current item price
        if form.cleaned_data["amount"] <= current_price:
            return HttpResponse("Error: Bid too low. Enter a bid greater than the current listed price.")

        # Save updated listing and bid
        form.instance.bidder = request.user
        form.instance.listing = listing
        bid = form.save(commit=False)
        bid.save()
        listing.highest_bid = bid
        listing.save()
        return HttpResponseRedirect(f"/listing/{listing_id}")

    else:
        return HttpResponse("Invalid form entry.")


# Renders a page with a ListingForm that allows the user to create a listing
@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            # Set the 'listed_by' field to the currently logged-in user
            form.instance.listed_by = request.user
            listing = form.save(commit=False)
            listing.save()
            return HttpResponseRedirect(f"/listing/{listing.id}")  # Redirect to a new URL
        else:
            return HttpResponse("Invalid form entry.")

    else:  # GET path
        form = ListingForm()
        return render(request, "auctions/create_listing.html", {"form": form})


# Renders a list of items filtered by the category the user selected
def browse_category(request, name):
    return render(request, f"auctions/index.html", {
        "listings": Listings.objects.filter(category=name, is_active=True),
        "header": f"Items by category: {name}"
    })


# Allows signed-in users to add comments on a listing page using a CommentForm
@login_required
def comment(request, listing_id):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("index"))

    # POST path
    form = CommentForm(request.POST)
    if form.is_valid():
        # Save updated listing and bid
        form.instance.user = request.user
        form.instance.listing = Listings.objects.get(pk=listing_id)
        comment = form.save(commit=False)
        comment.save()
    else:
        return HttpResponse("Invalid form entry.")

    return HttpResponseRedirect(f"/listing/{listing_id}")


# Allows users to end an auction on their items. The listing is set to inactive and
# the user with the highest bid is made the winner.
@login_required
def deactivate_listing(request, listing_id):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("index"))

    listing = Listings.objects.get(pk=listing_id)
    if request.POST.get("action") == "deactivate":
        listing.is_active = False

        if listing.highest_bid is None:  # No bids were placed on the item
            listing.save()
            return HttpResponse("Your auction has been closed. It did not receive any bids.")
        else:
            listing.winner = listing.highest_bid.bidder
            listing.save()

    return HttpResponseRedirect(f"/listing/{listing_id}")


# Allows a user to add or remove an item from their watchlist.
@login_required
def set_watchlist(request, listing_id):
    if request.method == "POST":
        listing = Listings.objects.get(pk=listing_id)
        user = request.user

        if request.POST.get("action") == "add_watchlist":
            user.watchlist.add(listing)
        elif request.POST.get("action") == "remove_watchlist":
            user.watchlist.remove(listing)

        user.save()

    return HttpResponseRedirect(f"/listing/{listing_id}")


# Displays the listings on the user's watchlist.
@login_required
def watch_list(request):
    return render(request, "auctions/index.html", {
        "listings": request.user.watchlist.all(),
        "header": "Your Watch List"
    })
