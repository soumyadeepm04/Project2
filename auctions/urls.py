from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listings, name = "create_listings"),
    path("listing/<int:listing_id>", views.listing_details, name = "listing_details"),
    path("add_watchlist/<int:listing_id>", views.add_watchlist, name = "add_watchlist"),
    path("watchlist", views.watchlist, name = "watchlist"),
    path("remove_watchlist/<int:listing_id>", views.remove_watchlist, name = "remove_watchlist"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("close_listing/<int:listing_id>", views.close_listing, name = "close_listing")
]
