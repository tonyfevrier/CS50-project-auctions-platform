from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addtowatchlist/<int:id>", views.addtowatchlist, name="addtowatchlist"),
]
