from django.urls import path
from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page>", views.getpage, name="getpage"),
    path("wiki/", views.getpage, name="wiki"),
    path("search/", views.search, name="search"),
    path("newpage/", views.newpage, name="newpage"),
    path("random/", views.random, name="randompage"),
    path("edit/<str:page>", views.edit, name="editpage"),
    path("edit/", views.edit, name="edit"),
    path("save/", views.save, name="save"),
]