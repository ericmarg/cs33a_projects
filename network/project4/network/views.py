import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.db import IntegrityError
from django.db.models import Model
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import PostForm
from .models import User, Post, Following

POSTS_PER_PAGE = 10  # Number of posts displayed per page by paginator


# noinspection DuplicatedCode
def index(request):
    # Flow to create a new post
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse('Login required.')

        form = PostForm(request.POST)
        if form.is_valid():
            # Set the user field
            form.instance.user = request.user

            # Save the post
            post = form.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponse('Invalid form entry.')

    # GET path
    page_number = request.GET.get('page')  # Get the page number from the query string
    if page_number is None:
        page_number = 1  # Default to page 1 if not specified
    else:
        page_number = int(page_number)

    # Retrieve all posts in reverse chronological order
    posts = Post.objects.all().order_by('-timestamp')
    p = Paginator(posts, POSTS_PER_PAGE)

    try:
        current_page = p.page(page_number)
    except EmptyPage:
        current_page = p.page(1)  # Handle invalid page number by defaulting to page 1

    form = PostForm()   # Form to create new posts
    return render(request, 'network/index.html', {
        'form': form,
        'posts': current_page.object_list,
        'pages': [p.page(i) for i in p.page_range],
        'current_page': current_page,
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
def update_post(request, post_id):
    # POST path for editing posts
    if request.method == 'POST':
        # Get the updated post content from the JSON object
        data = json.loads(request.body)
        content = data.get('content')

        # Retrieve the post from the database
        post = Post.objects.get(pk=post_id)
        if post is None:
            # Handle post not found
            return JsonResponse({
                "error": "Post not found."
            }, status=404)
        elif request.user != post.user:
            # Ensure posts are only editable by the poster
            return JsonResponse({
                "error": "Unauthorized."
            }, status=403)
        else:
            # Save the edited post
            post.content = content
            post.save()
            return JsonResponse({'message': 'Post edited successfully.'}, status=200)

    # PUT path for liking posts
    elif request.method == 'PUT':
        # Retrieve the post from the database
        try:
            post = Post.objects.get(pk=post_id)
        except Model.DoesNotExist:
            return JsonResponse({'error': 'Post not found.'}, status=404)

        user = request.user
        # Check if the user already liked the post
        if user in post.likes.all():
            # If the user previously liked the post, un-like it
            post.likes.remove(user)
        else:
            # Like the post
            post.likes.add(user)

        # Save the post and return the updated likes count
        post.save()
        return JsonResponse(post.likes.count(), status=200, safe=False)
    elif request.method == 'GET':
        try:
            # Return the post details in JSON format
            post = Post.objects.get(pk=post_id)
            return JsonResponse(post.serialize())
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found.'}, status=404)


@csrf_exempt
def profile(request, user_id):
    try:
        # Retrieve the user whose profile is being viewed
        viewed_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found.'}, status=404)

    follow_obj = None   # Create an instance of a Following object
    already_following = False
    if request.user.is_authenticated:
        # Check if the active user is following the viewed user
        try:
            # The active user follows the viewed user already
            follow_obj = Following.objects.get(follower=request.user, followee=viewed_user)
            already_following = True
        except Following.DoesNotExist:
            # Active user does not follow the user they are viewing
            already_following = False

    if request.method == 'POST':
        # Check if the Following instance already exists
        if follow_obj is None:
            # Following instance doesn't exist, create a new one
            follow_obj = Following.objects.create(follower=request.user, followee=viewed_user)

        # Update the relationships
        if already_following:
            # Unfollow the user
            viewed_user.followers.remove(follow_obj)
            request.user.following.remove(follow_obj)
        else:
            # Follow the user
            viewed_user.followers.add(follow_obj)
            request.user.following.add(follow_obj)

        # Save the user objects and return new follower count
        viewed_user.save()
        request.user.save()
        return JsonResponse({
            'unfollow': already_following,
            'follower_count': viewed_user.followers.count()
        }, status=200)

    # GET path
    # Pagination
    page_number = request.GET.get('page')  # Get the page number from the query string
    if page_number is None:
        page_number = 1  # Default to page 1 if not specified
    else:
        page_number = int(page_number)

    # Retrieve the posts from the user whose profile is being viewed
    posts = Post.objects.filter(user=viewed_user).order_by('-timestamp')
    p = Paginator(posts, POSTS_PER_PAGE)

    try:
        current_page = p.page(page_number)
    except EmptyPage:
        current_page = p.page(1)  # Handle invalid page number by defaulting to page 1

    return render(request, 'network/profile.html', {
        'viewed_user': viewed_user,
        'following': already_following,
        'posts': current_page.object_list,
        'pages': [p.page(i) for i in p.page_range],
        'current_page': current_page
    })


@login_required
def following(request):
    page_number = request.GET.get('page')  # Get the page number from the query string
    if page_number is None:
        page_number = 1  # Default to page 1 if not specified
    else:
        page_number = int(page_number)  # Convert the page number to an integer

    # Get the set of users that the active user is following
    users_following = [follow_obj.followee for follow_obj in request.user.following.all()]
    # Get posts from users that the active user is following
    posts = Post.objects.filter(user__in=users_following).order_by('-timestamp')

    # Pagination logic
    p = Paginator(posts, POSTS_PER_PAGE)
    try:
        current_page = p.page(page_number)
    except EmptyPage:
        current_page = p.page(1)  # Handle invalid page number by defaulting to page 1

    form = PostForm()   # Form to create a new post
    return render(request, 'network/index.html', {
        'form': form,
        'posts': current_page.object_list,
        'pages': [p.page(i) for i in p.page_range],
        'current_page': current_page,
    })
