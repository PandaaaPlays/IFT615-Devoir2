import uuid

from ActionLayer import ROCKET, CARGO


def load(cargo, rocket, location_from):
    print(f" - LOAD {cargo.name} dans {rocket.name} a partir de {location_from.name}")
    new_rocket = rocket.copy()
    new_cargo = cargo.copy()
    new_rocket.add_cargo(cargo)
    new_cargo.location = None
    return new_cargo, new_rocket


def unload(cargo, rocket, location_to):
    print(f" - UNLOAD {cargo.name} de {rocket.name} a {location_to.name}")
    new_rocket = rocket.copy()
    new_cargo = cargo.copy()
    new_rocket.remove_cargo(cargo)
    new_cargo.location = location_to
    return new_cargo, new_rocket


def move(rocket, location_to, location_from):
    print(f" - MOVE {rocket.name} de {location_from.name} a {location_to.name}")
    new_rocket = rocket.copy()
    new_rocket.set_location(location_to)
    new_rocket.set_has_fuel(False)
    return new_rocket
