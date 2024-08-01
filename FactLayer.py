from Operators import move, load
from Utils import find_in_list


def create_fact_layer(action_layer, facts):
    fact_layer = list(facts)
    for action, params in action_layer:
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

                fact_layer.append(move(rocket, location_to, location_from))

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

                fact_layer.append(new_rocket)
                fact_layer.append(new_cargo)

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

                new_cargo, new_rocket = load(cargo, rocket, to_location)

                fact_layer.append(new_rocket)
                fact_layer.append(new_cargo)

    return fact_layer