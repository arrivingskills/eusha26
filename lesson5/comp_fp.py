from dataclasses import dataclass, replace

@dataclass(frozen=True)
class Vehicle:
    name: str
    speed: float = 0.0
    fuel: float = 0.0

def drive(vehicle: Vehicle, distance: float) -> Vehicle:
    if distance <= 0:
        raise ValueError("Distance must be positive")
    
    new_fuel = vehicle.fuel - (distance * 0.1)
    new_speed = distance / 10
    
    return replace(vehicle, fuel=new_fuel, speed=new_speed)

def refuel(vehicle: Vehicle, amount: float) -> Vehicle:
    if amount <= 0:
        raise ValueError("Amount must be positive")
    
    return replace(vehicle, fuel=vehicle.fuel + amount)

def validate_fuel(vehicle: Vehicle) -> float:
    if vehicle.fuel <= 0:
        raise ValueError("Out of fuel")
    return vehicle.fuel

if __name__ == "__main__":
    # Initial state
    v1 = Vehicle(name="Interceptor")
    print(f"Initial: {v1}")

    # Refuel
    v2 = refuel(v1, 50)
    print(f"After refueling: {v2}")

    # Drive
    try:
        fuel_level = validate_fuel(v2)
        print(f"Fuel level before driving: {fuel_level}")
        
        v3 = drive(v2, 100)
        print(f"After driving 100km: {v3}")
        
        # Original v2 is unchanged
        print(f"v2 still has: {v2.fuel} fuel")
        
    except ValueError as e:
        print(f"Error: {e}")

    # Chaining operations (functional style)
    try:
        final_state = drive(refuel(v1, 20), 50)
        print(f"Chained result: {final_state}")
    except ValueError as e:
        print(f"Error: {e}")
