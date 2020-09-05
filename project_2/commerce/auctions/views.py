from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Auctions, Watchlist, Bids, Comments, History
import os


def create(request):
    if request.method == "POST" and request.user.is_authenticated:
        f = Auctions(
            name = request.POST["title"],
            condition = request.POST["condition"],
            description = request.POST["description"],
            image = request.POST["image"],
            availability = request.POST["quantity"],
            start_bid = request.POST["start_bid"],
            category = request.POST["category"],
            user = User.objects.get(id = request.user.id)
        )
        f.save()
        return HttpResponseRedirect(reverse("item", args=( f.id,) ))
    return render(request, "auctions/create.html", {
        "categories":return_categories(),
        "conditions":return_conditions()
    })


def item(request, item_id):
    item = Auctions.objects.filter(id = item_id).values().first()
    seller_id = item["user_id"]
    seller = User.objects.filter(id = seller_id).values().first()['username']
    user_id = request.user.id

    try:
        comments = []
        for i in Comments.objects.filter(item = item_id).order_by("id").values():
            dictionary = {}
            dictionary["username"] = User.objects.filter(id = i["user_id"]).values().first()["username"]
            dictionary["comment"] = i["comment"]
            comments.append(dictionary)
    except:
        comments = ["No comments yet"]

    try:
        if item_id == Watchlist.objects.filter(item_id = item_id, user_id = user_id).values().first()["item_id"]:
            watchlist_status = "Remove from Watchlist"
    except:
        watchlist_status = "Add to Watchlist"

    try:
        min_bid = item['buy_price']
        highest_bidder_id = item['buyer_id']
        highest_bidder = User.objects.filter(id = highest_bidder_id).values().first()["username"]
    except:
        try:
            bid = Bids.objects.filter(item_id = item_id).order_by("-bid").values().first()
            min_bid = bid['bid']
            highest_bidder_id = bid['user_id']
            highest_bidder = User.objects.filter(id = highest_bidder_id).values().first()["username"]
        except:
            min_bid = item['start_bid']
            highest_bidder_id = ""
            highest_bidder = ""

    return render(request, "auctions/item.html", {
        "item":item,
        "seller":seller,
        "watchlist":watchlist_status,
        "min_bid":min_bid,
        "highest_bidder_id":highest_bidder_id,
        "highest_bidder":highest_bidder,
        "comments":comments,
        "status":item['status'],
    })


def bid(request, item_id):
    if request.method == "POST" and request.user.is_authenticated:
        user_id = request.user.id
        item_bids = []
        for i in Bids.objects.filter(user_id = user_id).values():
            item_bids.append(i['item_id'])
        if item_id in item_bids:
            b = Bids.objects.get(user_id = user_id, item_id = item_id)
            b.bid = request.POST["bid"]
            b.save()
            return HttpResponseRedirect(reverse("item", args=(item_id,)))
        b = Bids (
            user = User.objects.get(id = request.user.id),
            item = Auctions.objects.get(id = item_id),
            quantity = request.POST["quantity"],
            bid = request.POST["bid"]
        )
        b.save()
        return HttpResponseRedirect(reverse("item", args=(item_id,)))


def change_watchlist(request, item_id):
    if request.method == "POST" and request.user.is_authenticated:
        user_id = request.user.id
        items_watchlist = set()
        try:
            for i in Watchlist.objects.filter(user_id = request.user.id).values():
                items_watchlist.add(i['item_id'])
            if item_id in items_watchlist:
                Watchlist.objects.filter(item_id = item_id, user_id = user_id).delete()
                return HttpResponseRedirect(reverse("item", args=(item_id,)))
        except:
            pass
        w = Watchlist (
            item = Auctions.objects.get(id = item_id),
            user = User.objects.get(id = request.user.id)
        )
        w.save()
        return HttpResponseRedirect(reverse("item", args=(item_id,)))


def close(request, item_id):
    bid = Bids.objects.filter(item_id = item_id)
    item = Auctions.objects.filter(id = item_id)

    if not bid:
        item.delete()

    try:
        buyer = bid.order_by("-bid").values().first()['user_id']
        seller = item.values().first()['user_id']

        h = History(
            buyer = User.objects.get(id = buyer),
            seller = User.objects.get(id = seller),
            price = bid.order_by("-bid").values().first()['bid'],
            quantity = bid.values().first()['quantity'],
            item = item.first()
        )
        h.save()

        if item.values().first()['availability'] == 1: 
            item.update(status = 0, availability = 0)
        elif item.values().first()['availability'] > 1:
            availability = item.values().first()['availability']
            item.update(availability = availability - bid.values().first()['quantity'])
        
        bid.delete()
        Watchlist.objects.filter(item_id = item_id).delete()

        return HttpResponseRedirect(reverse("item", args=(item_id,)))
    except:
        return HttpResponseRedirect(reverse("index"))


def comment(request, item_id):
    if request.method == "POST":
        c = Comments (
        user = User.objects.get(id = request.user.id),
        item = Auctions.objects.get(id = item_id),
        comment = request.POST["comment"]
        )
        c.save()
        return HttpResponseRedirect(reverse("item", args=(item_id,)))


#### Functions rendered by aux function show ####


def show(request, items, pagename):
    try:
        return render(request, "auctions/show.html", {
            "items":items,
            "pagename":pagename
        })
    except:
        return render(request, "auctions/show.html", {
            "items":[],
            "pagename":pagename
        })    


def index(request):
    return show(request, Auctions.objects.filter(status = 1).values(), "Active Listings")        


def mylistings(request):
    if request.user.is_authenticated:
        return show(request, Auctions.objects.filter(status = 1, user_id = request.user.id).values(), "My Active Listings")
    
    
def watchlist(request):
    items = []
    for i in Watchlist.objects.filter(user_id = request.user.id).values():
        items.append(Auctions.objects.filter(id = i["item_id"]).values().first())
    return show(request, items, "Watchlist")


#### Functions rendered by aux function show_hist ####


def show_hist(request, items, pagename, side):
    try:
        return render(request, "auctions/history.html", {
            "items":items,
            "pagename":pagename,
            "side":side
        })
    except:
        return render(request, "auctions/history.html", {
            "items":[],
            "pagename":pagename,
            "side":side
        })    


def buy_history(request):
    if request.user.is_authenticated:
        buy_sell_side = True
        
        items = []
        for item in History.objects.filter(buyer = request.user.id).values():
            li = Auctions.objects.filter(id = item['item_id']).values().first()
            li['buyer_username'] = User.objects.filter(id = item['buyer_id']).values().first()['username']
            li['seller_username'] = User.objects.filter(id = item['seller_id']).values().first()['username']
            li['price'] = item['price']
            li['quantity'] = item['quantity']
            items.append(li)
        return show_hist(request, items, "Buy History", buy_sell_side)


def sell_history(request):
    if request.user.is_authenticated:
        buy_sell_side = False

        items = []
        for item in History.objects.filter(seller = request.user.id).values():
            li = Auctions.objects.filter(id = item['item_id']).values().first()
            li['buyer_username'] = User.objects.filter(id = item['buyer_id']).values().first()['username']
            li['seller_username'] = User.objects.filter(id = item['seller_id']).values().first()['username']
            li['price'] = item['price']
            li['quantity'] = item['quantity']
            items.append(li)
        return show_hist(request, items, "Sell History", buy_sell_side)


#### Category related ####


def categories(request):
    return render(request, "auctions/categories.html",{
        "categories":return_categories()
    })


def category(request, category):
    items = []
    for i in Auctions.objects.filter(category=category, status = 1).values():
        items.append(i)
    return render(request, "auctions/category.html", {
        "items":items,
        "category":category
    })


### Get starting functions ###


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
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Ensure password matches confirmation
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


## Auxiliary functions ##


def return_categories():
    path = os.getcwd()
    file_dir = path + "\\categories.txt"
    f = open(file_dir, "r").read()
    categories = f.split("\n")
    return categories


def return_conditions():
    path = os.getcwd()
    file_dir = path + "\\conditions.txt"
    f = open(file_dir, "r").read()
    conditions = f.split("\n")
    return conditions
