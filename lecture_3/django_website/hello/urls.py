from django.urls import path
from . import views

app_name = "hello"
urlpatterns = {
    path("", views.index, name="index"),
    path("brunno", views.brunno, name="brunno"),
    path("<str:name>", views.greet, name="greet")
}