from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("mylistings", views.mylistings, name="mylistings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:item_id>", views.change_watchlist, name="change_watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category, name="category"),
    path("item/<int:item_id>", views.item, name="item"),
    path("bid/<int:item_id>", views.bid, name="bid"),
    path("close/<int:item_id>", views.close, name="close"),
    path("buyhistory", views.buy_history, name="buy_history"),
    path("sellhistory", views.sell_history, name="sell_history"),
    path("comment/<int:item_id>", views.comment, name="comment")
]
