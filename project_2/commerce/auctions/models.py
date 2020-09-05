from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaulttags import register


class User(AbstractUser):
    pass


class Auctions(models.Model):
    name = models.CharField(max_length=64, null=True)
    condition = models.CharField(max_length=16, null=True)
    description = models.CharField(max_length=512, null=True)
    image = models.CharField(max_length=256, null=True)
    category = models.CharField(max_length=64, null=True)
    availability = models.IntegerField(null=True)
    start_bid = models.DecimalField(null=True, decimal_places=2, max_digits=9)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    status = models.BooleanField(default=True)


class Watchlist(models.Model):
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)
    item = models.ForeignKey(Auctions, null=True, default=None, on_delete=models.CASCADE)


class Bids(models.Model):
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)
    item = models.ForeignKey(Auctions, null=True, default=None, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, default=None)
    bid = models.DecimalField(max_length=500, decimal_places=2, max_digits=12, null=True)


class Comments(models.Model):
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)
    item = models.ForeignKey(Auctions, null=True, default=None, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, null=True)


class History(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer", null=True, default=None)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller", null=True, default=None)
    price = models.DecimalField(null=True, default=None, decimal_places=2, max_digits=9)
    quantity = models.IntegerField(null=True, default=None)
    item = models.ForeignKey(Auctions, null=True, default=None, on_delete=models.CASCADE)

