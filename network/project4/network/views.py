import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post
from .forms import PostForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Set the user field
            form.instance.user = request.user
            listing = form.save(commit=False)
            listing.save()
            # Create a new instance of the form to clear the fields
            form = PostForm()
            return HttpResponseRedirect('/')
        else:
            return HttpResponse('Invalid form entry.')

    page_number = request.GET.get('page')  # Get the page number from the query string
    if page_number is None:
        page_number = 1  # Default to page 1 if not specified
    else:
        page_number = int(page_number)  # Convert the page number to an integer

    posts = Post.objects.all().order_by('-timestamp')
    p = Paginator(posts, 10)

    try:
        current_page = p.page(page_number)
    except EmptyPage:
        current_page = p.page(1)  # Handle invalid page number by defaulting to page 1

    form = PostForm()
    return render(request, 'network/index.html', {
        'form': form,
        'posts': current_page.object_list,
        'pages': [p.page(i) for i in p.page_range],
        'current_page': current_page
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
@login_required
def post(request, post_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        content = data.get('content')
        post = Post.objects.get(pk=post_id)
        if post is None:
            return JsonResponse({
                "error": "Post not found."
            }, status=400)
        else:
            post.content = content
            post.save()
            return render(request, "network/register.html")
    elif request.method == 'PUT':
        # User liked/unliked the post
        post = Post.objects.get(pk=post_id)
        user = request.user

        # Check if the user already liked the post
        if user in post.likes.all():
            # If the user previously liked the post, un-like it
            post.likes.remove(user)
            post.like_count -= 1
        else:
            # Like the post
            post.likes.add(user)
            post.like_count += 1

        post.save()
        return HttpResponse(status=200)
    elif request.method == 'GET':
        try:
            # Return the post details in JSON format
            post = Post.objects.get(pk=post_id)
            return JsonResponse(post.serialize())
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found.'}, status=404)
