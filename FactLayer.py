from Operators import move, load, unload
from Utils import find_with_obj


def create_fact_layer(action_layer, facts):
    fact_layer = set(facts)
    for action in action_layer:
        apply_effects(action, facts, fact_layer)

    return fact_layer

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

            if location_from.name != location_to.name:
                new_rocket = move(rocket, location_to, location_from)
                new_rocket.set_action(action)
                list_to_apply.add(new_rocket)

            return rocket

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
            new_cargo.set_action(action)
            new_rocket.set_action(action)

            list_to_apply.add(new_rocket)
            list_to_apply.add(new_cargo)

            return (rocket, cargo)

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
            new_cargo.set_action(action)
            new_rocket.set_action(action)

            list_to_apply.add(new_cargo)
            list_to_apply.add(new_cargo)

            return (rocket, cargo)