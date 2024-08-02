import uuid

from ActionLayer import ROCKET, CARGO


def load(cargo, rocket, location_from):
    print(f"Trying : LOAD {cargo.name} in {rocket.name} from {location_from.name}")
    new_rocket = rocket.copy()
    new_cargo = cargo.copy()
    new_rocket.add_cargo(cargo)
    new_cargo.location = None
    return new_cargo, new_rocket


def unload(cargo, rocket, location_to):
    print(f"Trying : UNLOAD {cargo.name} from {rocket.name} at {location_to.name}")
    new_rocket = rocket.copy()
    new_cargo = cargo.copy()
    new_rocket.remove_cargo(cargo)
    new_cargo.location = location_to
    return new_cargo, new_rocket


def move(rocket, location_to, location_from):
    print(f"Trying : MOVE {rocket.name} from {location_from.name} to {location_to.name}")
    new_rocket = rocket.copy()
    new_rocket.set_location(location_to)
    new_rocket.set_has_fuel(False)
    return new_rocket
