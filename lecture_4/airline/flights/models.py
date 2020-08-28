from django.db import models

# Create your models here.

class Airports(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.code} ({self.city})"

class Flights(models.Model):
    origin = models.ForeignKey(Airports, on_delete=models.PROTECT, related_name="departures")
    destination = models.ForeignKey(Airports, on_delete=models.PROTECT, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"Flight {self.id}: {self.origin} to {self.destination}"

class Passengers(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flights, blank=True, related_name="passengers")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
