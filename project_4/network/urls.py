
from django.urls import path

from . import views

urlpatterns = [
    path("<int:page>", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<str:username>/<int:page>", views.user, name="username"),
    path("user/<str:username>/following/<int:page>", views.following, name="following"),

    ################ API's ################
    path("API/post", views.post, name='post'),
    path("API/follow", views.follow, name='follow'),
    path("API/unfollow", views.unfollow, name='unfollow'),
    path("API/delete/<int:id>", views.delete, name='delete_post'),
    path("API/save", views.save, name='save_post'),
    path("API/like", views.like, name='like_post'),
    path("API/unlike", views.unlike, name='like_post'),
]
