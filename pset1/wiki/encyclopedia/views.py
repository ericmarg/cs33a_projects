from django.http import HttpResponse
from django.shortcuts import render, redirect
from random import choice
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def get_wiki(request, name):
    try:
        return render(request, "encyclopedia/entry.html", {
            "page": markdown2.markdown(util.get_entry(name)),
            "name": name
        })
    except TypeError:
        return redirect("/404.html")


def search(request):
    # Retrieve the user query from the GET request using Django's API
    query = request.GET.get("q")

    # Get the queried entry if it exists
    test = util.get_entry(query)

    # Check for a return. If None, we want to redirect to the search page.
    if test is None:
        return render(request, "encyclopedia/search.html", {
            # Create a list of pages whose title contains the substring the user queried
            "matches": list(entry for entry in util.list_entries() if entry.find(query) > 0)
        })

    # The entry was found; render the page.
    return render(request, "encyclopedia/entry.html", {
        "page": markdown2.markdown(util.get_entry(query)),
        "name": query
    })


def create_new_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if util.get_entry(title) is None:
            content = request.POST.get('content')
            util.save_entry(title, content)
            return redirect(f'/wiki/{title}')
        else:
            return HttpResponse(f'Error: page {title} already exists!')

    # GET path
    return render(request, "encyclopedia/newpage.html")


def edit_page(request, name):
    if request.method == 'POST':
        content = request.POST.get('content')
        util.save_entry(name, content)
        return redirect(f'/wiki/{name}')

    return render(request, "encyclopedia/editpage.html", {
        'content': util.get_entry(name),
        "name": name
    })


def random(request):
    # Pick a random page name from all the entries
    name = choice(util.list_entries())

    # Render the randomly chosen page
    return render(request, "encyclopedia/entry.html", {
        "page": markdown2.markdown(util.get_entry(name)),
        "name": name
    })
