import datetime
import json

from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Puzzle

WORDS_PER_ROW = 4


def index(request):
    return render(request, "connections/index.html")


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
            return render(request, "connections/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "connections/login.html")


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
            return render(request, "connections/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "connections/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "connections/register.html")


@csrf_exempt
def play(request, date=None):
    # Use the supplied date or default to today"s date
    if not date:
        date = datetime.date.today()

    try:
        # Get the first puzzle with the given date (there should only be one)
        puzzle = Puzzle.objects.get(date=date)
    except ObjectDoesNotExist:
        # Get the first puzzle in the database
        puzzle = Puzzle.objects.all()[0]

    if request.method == "POST":
        return JsonResponse([puzzle.puzzle, puzzle.number], safe=False)

    # Create a 2-D list of words to populate the puzzle grid from puzzle.puzzle
    # puzzle.puzzle is a dictionary of dictionaries
    rows = [list(inner_dict.values())[0] for inner_dict in puzzle.puzzle.values()]

    return render(request, "connections/play.html", {
        "rows": rows,
        "date": date,
        "WORDS_PER_ROW": WORDS_PER_ROW
    })


def stats(request):
    solved = request.user.solved.all()
    return render(request, f"connections/stats.html", {
        "solved": solved
    })


@csrf_exempt
def mark_puzzle_solved(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        puzzle_number = data.get("number")
        try:
            puzzle = Puzzle.objects.get(number=puzzle_number)
            try:
                user = User.objects.get(username=request.user)

                # Add the puzzle to the user"s solved puzzles
                user.solved.add(puzzle)
                user.save()
                return JsonResponse({"message": "Puzzle marked as solved successfully."})
            except User.DoesNotExist:
                return JsonResponse({"message": "Progress not save; user not signed in."}, status=200)

        except Puzzle.DoesNotExist:
            return JsonResponse({"error": "Invalid puzzle number."}, status=400)

    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)


def play_archived_puzzle(request):
    puzzles = Puzzle.objects.all()
    return render(request, "connections/archive.html", {
        "puzzles": puzzles
    })
