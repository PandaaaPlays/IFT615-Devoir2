from ActionLayer import CARGO, ROCKET
from Operators import move, load, unload
from Utils import find_with_obj

# Creation d'une fact layer en se basant sur la precedente
def create_fact_layer(action_layer, facts):
    fact_layer = set(facts)
    for action in action_layer:
        apply_effects(action, facts, fact_layer)

    return fact_layer

# Appliquer les effets des actions sur les facts et les ajouter dans la liste
def apply_effects(action, facts, list_to_apply):
    params = action.params
    match action.operator.name:
        case 'MOVE':
            type = action.operator.effects[0].object_types[0].strip('()')
            obj = params[type]
            rocket = find_with_obj(facts, obj)

            type = action.operator.effects[0].object_types[1].strip('()')
            obj = params[type]
            location_to = find_with_obj(facts, obj)

            type = action.operator.effects[2].object_types[2].strip('()')
            obj = params[type]
            location_from = find_with_obj(facts, obj)

            new_rocket = None
            if location_from.name != location_to.name:
                new_rocket = move(rocket, location_to, location_from)
                new_rocket.add_action(action)
                add(new_rocket, list_to_apply)

            return new_rocket

        case 'LOAD':
            type = action.operator.effects[0].object_types[0].strip('()')
            obj = params[type]
            cargo = find_with_obj(facts, obj)

            type = action.operator.effects[0].object_types[1].strip('()')
            obj = params[type]
            rocket = find_with_obj(facts, obj)

            type = action.operator.effects[1].object_types[2].strip('()')
            obj = params[type]
            location_from = find_with_obj(facts, obj)

            new_cargo, new_rocket = load(cargo, rocket, location_from)
            new_cargo.add_action(action)
            new_rocket.add_action(action)

            add(new_rocket, list_to_apply)
            add(new_cargo, list_to_apply)

            return (new_rocket, new_cargo)

        case 'UNLOAD':
            type = action.operator.effects[0].object_types[0].strip('()')
            obj = params[type]
            cargo = find_with_obj(facts, obj)

            type = action.operator.effects[0].object_types[1].strip('()')
            obj = params[type]
            to_location = find_with_obj(facts, obj)

            type = action.operator.effects[1].object_types[2].strip('()')
            obj = params[type]
            rocket = find_with_obj(facts, obj)

            new_cargo, new_rocket = unload(cargo, rocket, to_location)
            new_cargo.add_action(action)
            new_rocket.add_action(action)

            add(new_rocket, list_to_apply)
            add(new_cargo, list_to_apply)

            return (new_rocket, new_cargo)


# Ajout dans la list, ou simplement ajout de l'action si deja dans la liste
def add(object, list_to_apply):
    added = False
    for obj in list_to_apply:
        if isinstance(object, CARGO):
            if isinstance(obj, CARGO) and obj.action:
                if obj.name == object.name and obj.location == object.location:
                    for action in object.action:
                        obj.add_action(action)
                        added = True
                    break

        if isinstance(object, ROCKET):
            if isinstance(obj, ROCKET) and obj.action:
                if obj.name == object.name and obj.location == object.location and obj.has_fuel == object.has_fuel and obj.cargo == object.cargo:
                    for action in object.action:
                        obj.add_action(action)
                        added = True
                    break
    if not added:
        list_to_apply.add(object)