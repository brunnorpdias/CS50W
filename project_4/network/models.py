from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("self", symmetrical=False, related_name="user_followers")
    following = models.ManyToManyField("self", symmetrical=False, related_name="user_following")

class Post(models.Model):
    username = models.ForeignKey(User, on_delete=models.PROTECT)
    content = models.TextField(null=False)
    date = models.DateTimeField(null=False)
    likes = models.ManyToManyField(User, related_name="like_users")
