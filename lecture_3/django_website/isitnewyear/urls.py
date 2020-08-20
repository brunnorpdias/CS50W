from django.urls import path
from . import views

app_name = "isitnewyear"
urlpatterns = [
    path("", views.index, name="index")
]