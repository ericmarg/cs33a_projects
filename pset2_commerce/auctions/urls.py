from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("admin/", admin.site.urls),
    path("listing/<int:listing_id>", views.get_listing, name="listing_id"),
    path("categories", views.categories, name="categories"),
    path("browse_category/<str:name>", views.browse_category, name="category"),
    path("create_listing/", views.create_listing, name="create_listing"),
    path("bid/<int:listing_id>/", views.bid, name="bid"),
    path("comment/<int:listing_id>/", views.comment, name="comment"),
    path("deactivate/<int:listing_id>/", views.deactivate_listing, name="deactivate_listing"),
    path("set_watchlist/<int:listing_id>", views.set_watchlist, name="set_watchlist"),
    path("watch_list", views.watch_list, name="watch_list")
]
