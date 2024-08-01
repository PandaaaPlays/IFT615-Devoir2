import uuid

from ActionLayer import ROCKET, CARGO


def load(cargo, rocket, location_from):
    new_rocket = rocket.__copy__()
    new_cargo = cargo.__copy__()
    new_rocket.add_cargo(cargo)
    new_cargo.location = None
    return new_cargo, new_rocket


def unload(cargo, rocket, location_to):
    print(f"Unloading {cargo.name} from {rocket.name} at {location_to.name}")
    new_rocket = rocket.__copy__()
    new_cargo = cargo.__copy__()
    new_rocket.remove_cargo(cargo)
    new_cargo.location = location_to
    return new_cargo, new_rocket


def move(rocket, location_to, location_from):
    new_rocket = ROCKET(rocket.name)
    new_rocket.set_location(location_to)
    new_rocket.set_has_fuel(False)
    return new_rocket
