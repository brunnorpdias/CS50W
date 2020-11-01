from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
# from django.urls import reverse (cant't reverse pages with parameter e.g., /1)
import json
from datetime import datetime as dt
from django.core.paginator import Paginator

from .models import User, Post


def index(request, page):
    data = Post.objects.order_by('-date').values()
    posts = []
    for i in data:
        i['username'] = User.objects.filter(id=i['username_id']).values().first()['username']

        try:
            like = Post.objects.get(id=i['id'], likes__username=request.user)
            i['like'] = True
        except:
            i['like'] = False

        i['n_likes'] = len(Post.objects.get(id=i['id']).likes.values())
        posts.append(i)

    paginator = Paginator(posts, 10)
    n_pages = paginator.num_pages
    p = paginator.page(page)

    return render(request, "network/index.html", {
        'posts':posts,
        'p':p,
        'n_pages':n_pages,
        'page':page,
    })

def user(request, username, page):
    list_followers = []
    for i in User.objects.filter(followers__username=username).values():
        list_followers.append(i['username'])

    n_followers = len(User.objects.filter(followers__username=username))
    n_following = len(User.objects.filter(following__username=username))

    data = Post.objects.filter(username_id=User.objects.filter(username=username).values('id').first()['id']).order_by('-date').values()
    posts = []
    for i in data:
        i['username'] = username
        try:
            like = Post.objects.get(id=i['id'], likes__username=request.user)
            i['like'] = True
        except:
            i['like'] = False

        i['n_likes'] = len(Post.objects.get(id=i['id']).likes.values())
        posts.append(i)


    paginator = Paginator(posts, 10)
    n_pages = paginator.num_pages
    p = paginator.page(page)


    return render(request, "network/userpage.html", {
        'username':username,
        'posts':posts,
        'p':p,
        'n_pages':n_pages,
        'page':page,
        'list_followers':list_followers,
        'n_followers':n_followers,
        'n_following':n_following,
    })


def following(request, username, page):
    following = ()
    for i in User.objects.filter(following__username=username).values('id'):
        following = following + (i['id'],)

    try:
        data = Post.objects.filter(username=following).order_by('-date').values()
    except:
        data = []


    posts = []
    for i in data:
        i['username'] = User.objects.filter(id=i['username_id']).values().first()['username']
        try:
            like = Post.objects.get(id=i['id'], likes__username=request.user)
            i['like'] = True
        except:
            i['like'] = False

        i['n_likes'] = len(Post.objects.get(id=i['id']).likes.values())
        posts.append(i)

    paginator = Paginator(posts, 10)
    n_pages = paginator.num_pages
    p = paginator.page(page)


    return render(request, "network/following.html", {
        'posts':posts,
        'p':p,
        'n_pages':n_pages,
        'page':page,
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
            return HttpResponseRedirect('/1')
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/1')


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect('/1')
    else:
        return render(request, "network/register.html")




############## API's ##################

def post(request):
    data = json.loads(request.body)

    post = Post(
        username=User.objects.get(username=data['username']),
        content=data['text'],
        date=dt.now()
    )
    post.save()

    return JsonResponse({'data':data})

def follow(request):
    data = json.loads(request.body)

    page_username = str(data['page_username']).replace(' ', '')
    username = str(data['username']).replace(' ', '')

    page_user = User.objects.get(username=page_username)
    user = User.objects.get(username=username)

    user.followers.add(page_user)
    page_user.following.add(user)
    return JsonResponse({'response':'OK', 'data':data})


def unfollow(request):
    data = json.loads(request.body)

    page_username = str(data['page_username']).replace(' ', '')
    username = str(data['username']).replace(' ', '')

    page_user = User.objects.get(username=page_username)
    user = User.objects.get(username=username)

    user.followers.remove(page_user)
    page_user.following.remove(user)
    return JsonResponse({'response':'OK', 'data':data})


def delete(request, id):
    post = Post.objects.get(id=id)
    post.delete()

    return JsonResponse({'response':'OK'})


def save(request):
    data = json.loads(request.body)
    
    post = Post.objects.get(id=int(data['id']))
    post.content = data['text']
    post.save()

    return JsonResponse({'response':'OK'})


def like(request):
    data = json.loads(request.body)

    post = Post.objects.get(id=int(data['id']))
    post.likes.add(User.objects.get(username=data['username']))
    post.save()

    return JsonResponse({'response':'OK', 'data':data})


def unlike(request):
    data = json.loads(request.body)

    post = Post.objects.get(id=int(data['id']))
    post.likes.remove(User.objects.get(username=data['username']))
    post.save()

    return JsonResponse({'response':'OK', 'data':data})