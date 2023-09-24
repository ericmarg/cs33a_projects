from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.get_wiki, name="wiki_page"),
    path("search/", views.search, name="search"),
    path("newpage/", views.create_new_page, name="newpage"),
    path("edit/<str:name>", views.edit_page, name="edit"),
    path("random/", views.random, name="random")
]
