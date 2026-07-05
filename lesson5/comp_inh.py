class Vehicle:
    def __init__(self, name):
        self.name = name
        self.speed = 0
        self.fuel = 0

    def drive(self, distance):
        if distance <= 0:
            raise ValueError("Distance must be positive")
        self.fuel -= distance * 0.1
        self.speed = distance / 10
        return self.speed, self.fuel
    def refuel(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.fuel += amount
    def validate_fuel(self):
        if self.fuel <= 0:
            raise ValueError("Out of fuel")
        return self.fuel

