from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Flights, Passengers

# Create your views here.

def index(request):
    return render(request, "flights/index.html",
    {"flights":Flights.objects.all()}
    )

def flight_info(request, flight_id):
    flight = Flights.objects.get(pk=flight_id)
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers":flight.passengers.all(),
        "non_passengers":Passengers.objects.exclude(flights=flight)
    })

def book(request, flight_id):
    if request.method == 'POST':
        flight = Flights.objects.get(pk=flight_id)
        passenger = Passengers.objects.get(pk=int(request.POST["passenger"]))
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("flights:flight", args=(flight_id,)))   #Args structured as a couple
        # Add verification for missing flights or passengers