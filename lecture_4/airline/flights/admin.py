from django.contrib import admin
from .models import Flights, Airports, Passengers

# Register your models here.

class FlightsAdmin(admin.ModelAdmin):
    list_display = ("id", "origin", "destination", "duration")

class PassengersAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",)

admin.site.register(Flights, FlightsAdmin)
admin.site.register(Airports)
admin.site.register(Passengers, PassengersAdmin)