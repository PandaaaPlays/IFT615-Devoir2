import ActionLayer
from Operators import move, load, unload
from Utils import find_in_list


def create_fact_layer(action_layer, facts):
    fact_layer = list(facts)
    for action, params in action_layer:
        apply_effects(action, params, facts, fact_layer)

    return fact_layer

def apply_effects(action, params, facts, list_to_apply):
    match action.name:
        case 'MOVE':
            type = action.effects[0].object_types[0].strip('()')
            obj = params[type]
            rocket = find_in_list(facts, obj.name)

            type = action.effects[0].object_types[1].strip('()')
            obj = params[type]
            location_to = find_in_list(facts, obj.name)

            type = action.effects[2].object_types[2].strip('()')
            obj = params[type]
            location_from = find_in_list(facts, obj.name)

            if location_to.name != location_from.name:
                list_to_apply.append(move(rocket, location_to, location_from))

            return rocket

        case 'LOAD':
            type = action.effects[0].object_types[0].strip('()')
            obj = params[type]
            cargo = find_in_list(facts, obj.name)

            type = action.effects[0].object_types[1].strip('()')
            obj = params[type]
            rocket = find_in_list(facts, obj.name)

            type = action.effects[1].object_types[2].strip('()')
            obj = params[type]
            location_from = find_in_list(facts, obj.name)

            new_cargo, new_rocket = load(cargo, rocket, location_from)

            list_to_apply.append(new_rocket)
            list_to_apply.append(new_cargo)

            return (rocket, cargo)

        case 'UNLOAD':
            type = action.effects[0].object_types[0].strip('()')
            obj = params[type]
            cargo = find_in_list(facts, obj.name)

            type = action.effects[0].object_types[1].strip('()')
            obj = params[type]
            to_location = find_in_list(facts, obj.name)

            type = action.effects[1].object_types[2].strip('()')
            obj = params[type]
            rocket = find_in_list(facts, obj.name)

            new_cargo, new_rocket = unload(cargo, rocket, to_location)

            list_to_apply.append(new_rocket)
            list_to_apply.append(new_cargo)

            return (rocket, cargo)