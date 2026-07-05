class ModeOfTransport:
    # airport, bus, train, tram, subway, taxi, car, boat, plane
    pass

class VehiclePurpose:
    # passenger, commercial, taxi, other

class Vehicle:
    def __init__(self):
        self.mode_of_transport = ModeOfTransport()
        self.vehicle_purpose = VehiclePurpose()
        self.passenger_count = 0

airplane = Vehicle()
airplane.mode_of_transport = ModeOfTransport.AIRPORT