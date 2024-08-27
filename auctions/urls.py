from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("toggletowatchlist/<int:id>", views.toggletowatchlist, name="toggletowatchlist"),
    path("listing/<int:id>/submitbid", views.submitbid, name="submitbid"),
    path("listing/<int:id>/deletelisting", views.deletelisting, name="deletelisting"),
    path("listing/<int:id>/savecomment", views.savecomment, name="savecomment"),
]
