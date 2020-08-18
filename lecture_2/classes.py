from numpy import random as rd


class Flight:
    def __init__(self, capacity):
        self.capacity = capacity
        self.passengers = []
        self.flight_n = rd.randint(0, 9999)

    def number(self):
        """
        Prints a 4 digit string representing the flight number
        """
        return str(self.flight_n).zfill(4)

    def add_passenger(self, name):
        if self.open_seats() == 0:
            return f"I'm sorry {name}, there aren't any seats on this flight"
        else:
            self.passengers.append(name)
            return f"Seat reserved! Thanks for flying with us, {name}"

    def open_seats(self):
        return self.capacity - len(self.passengers)


flight = Flight(3)
flight.add_passenger('Harry')
print(f'There are {flight.open_seats()} seats open flight {flight.number()}')
