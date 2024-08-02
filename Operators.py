import uuid

from ActionLayer import ROCKET, CARGO


def load(cargo, rocket, location_from):
    print(f"Loading {cargo.name} in {rocket.name}")
    new_rocket = rocket.copy()
    new_cargo = cargo.copy()
    new_rocket.add_cargo(cargo)
    new_cargo.location = None
    return new_cargo, new_rocket


def unload(cargo, rocket, location_to):
    print(f"Unloading {cargo.name} from {rocket.name} at {location_to.name}")
    new_rocket = rocket.copy()
    new_cargo = cargo.copy()
    new_rocket.remove_cargo(cargo)
    new_cargo.location = location_to
    return new_cargo, new_rocket


def move(rocket, location_to, location_from):
    print(f"Moving {rocket.name} from {location_from.name} to {location_to.name}")
    print(f"Bef {rocket.cargo}")
    new_rocket = rocket.copy()
    print(f"Aft {new_rocket.cargo}")
    new_rocket.set_location(location_to)
    new_rocket.set_has_fuel(False)
    return new_rocket
