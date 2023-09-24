import markdown2
from django.http import HttpResponse
from django.shortcuts import render, redirect
from random import choice
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
    except TypeError:   # Page not found
        return redirect("/404.html")


def search(request):
    # Retrieve the user query from the GET request using Django's API
    query = request.GET.get("q")

    # Check for an entry. If None, redirect to the search page.
    if util.get_entry(query) is None:
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
    if request.method == "POST":
        # Get the title from the form
        title = request.POST.get("title")

        # Check for an existing entry under that title
        if util.get_entry(title) is None:
            # There isn't an entry, so create a new one
            content = request.POST.get("content")
            util.save_entry(title, content)
            return redirect(f"/wiki/{title}")
        else:
            # Return an error message if there is already a page with that name
            return HttpResponse(f"Error: page {title} already exists!")

    # GET path; render the create-new-page template
    return render(request, "encyclopedia/newpage.html")


def edit_page(request, name):
    if request.method == "POST":
        # Get the updated content from the form
        content = request.POST.get("content")

        # Save the updated entry
        util.save_entry(name, content)
        return redirect(f"/wiki/{name}")

    # GET path; render a form with the text area pre-populated
    return render(request, "encyclopedia/editpage.html", {
        "content": util.get_entry(name),    # The existing page content
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
