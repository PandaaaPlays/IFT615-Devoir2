from Utils import find_in_list

def create_fact_layer(action_layer, facts):
    # Create a fact layer based on the action layer
    fact_layer = set(facts)
    for action, params in action_layer:
        print(f"Action: {action.name}")
        for effect in action.effects:
            apply_effect(effect, params, fact_layer)
            print(f" - Effect: {effect.operand} | {effect.object_types}")
    return fact_layer

def apply_effect(op_effect, param_dict, fact_layer):
    operand = op_effect.operand.strip('()')
    print(f"Applying effect with operand: {operand}")

    match operand:
        case 'in':
            type1 = op_effect.object_types[0].strip('()')
            obj1 = param_dict[type1]
            type2 = op_effect.object_types[1].strip('()')
            obj2 = param_dict[type2]
            print(f"Adding cargo: {obj1.name} to {obj2.name}")
            fact = find_in_list(fact_layer, obj2.name)
            if fact:
                fact.add_cargo(obj1)

        case 'del':
            match op_effect.object_types[0].strip('()'):
                case 'at':
                    type1 = op_effect.object_types[1].strip('()')
                    obj1 = param_dict[type1]
                    print(f"Removing location for: {obj1.name}")
                    type2 = op_effect.object_types[2].strip('()')
                    obj2 = param_dict[type2]
                    fact = find_in_list(fact_layer, obj1.name)
                    if fact:
                        fact.remove_location(obj2)

                case 'in':
                    type1 = op_effect.object_types[2].strip('()')
                    obj1 = param_dict[type1]
                    type2 = op_effect.object_types[1].strip('()')
                    obj2 = param_dict[type2]
                    print(f"Removing cargo: {obj1.name} from {obj2.name}")
                    fact = find_in_list(fact_layer, obj1.name)
                    if fact:
                        fact.remove_cargo(obj2)

                case 'has-fuel':
                    type1 = op_effect.object_types[1].strip('()')
                    obj1 = param_dict[type1]
                    print(f"Setting has_fuel to False for: {obj1.name}")
                    fact = find_in_list(fact_layer, obj1.name)
                    if fact:
                        fact.set_has_fuel(False)

        case 'at':
            type1 = op_effect.object_types[0].strip('()')
            obj1 = param_dict[type1]
            type2 = op_effect.object_types[1].strip('()')
            obj2 = param_dict[type2]
            print(f"Setting location of: {obj1.name} to {obj2.name}")
            fact = find_in_list(fact_layer, obj1.name)
            if fact:
                fact.add_location(obj2)