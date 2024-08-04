from itertools import product

from Objects import VariablePair, Fact, Action
from Utils import find_with_variable

class PLACE(Fact):
    def __init__(self, name, action):
        super().__init__(name)


class OBJECT(Fact):
    def __init__(self, name, action):
        super().__init__(name)
        self.location = None

    def set_location(self, location):
        self.location = location


class CARGO(OBJECT):
    def __init__(self, name, action):
        super().__init__(name, action)
        self.destination = None

    def set_destination(self, destination):
        self.destination = destination

    def copy(self):
        new_cargo = CARGO(self.name, self.action)
        new_cargo.set_destination(self.destination)
        new_cargo.location = self.location
        return new_cargo


class ROCKET(OBJECT):
    def __init__(self, name, action):
        super().__init__(name, action)
        self.has_fuel = False
        self.cargo = set()

    def set_has_fuel(self, has_fuel):
        self.has_fuel = has_fuel

    def add_cargo(self, cargo):
        self.cargo.add(cargo)

    def remove_cargo(self, cargo):
        self.cargo.discard(cargo)

    def copy(self):
        new_rocket = ROCKET(self.name, self.action)
        new_rocket.cargo = set(self.cargo)
        new_rocket.set_location(self.location)
        new_rocket.set_has_fuel(self.has_fuel)
        return new_rocket


def create_action_layer(fact_layer, operators):
    action_layer = []
    mutex_actions = set()

    print("Actions possible a cette iteration: ")

    for operator in operators:
        possible_params = [
            [fact for fact in fact_layer if isinstance(fact, eval(param.type))]
            for param in operator.params
        ]

        for param_combination in product(*possible_params):
            param_dict = {param.name: fact for param, fact in zip(operator.params, param_combination)}

            if preconditions_satisfied(operator, param_dict):
                action = Action(operator, param_dict)
                print(f" - {action.operator.name}")

                for existing_action in action_layer:
                    if are_actions_mutex(action, existing_action):
                        mutex_actions.add((action, existing_action))

                action_layer.append(action)

    print("Mutex Actions:")
    for action1, action2 in mutex_actions:
        print(f" - {action1.operator.name} a un mutex avec {action2.operator.name}")

    return action_layer, mutex_actions

# Si 2 actions sont mutuellement exclusives, elles sont de la même instance (check les param) et ont les mêmes "facts"
def are_actions_mutex(action1, action2):
    for param1, fact1 in action1.params.items():
        for param2, fact2 in action2.params.items():
            if isinstance(fact1, CARGO) and isinstance(fact2, CARGO) and fact1 == fact2:
                return True
            if isinstance(fact1, ROCKET) and isinstance(fact2, ROCKET) and fact1 == fact2:
                return True
    return False

# Les preconditions sont satisfaites ou non?
def preconditions_satisfied(operator, param_dict):
    params_list = [VariablePair(param, param_dict[param.name]) for param in operator.params]

    for precond in operator.preconds:
        if not check_precond(precond, params_list):
            return False
    return True


# Condition de preconditions (pour qu'elle soient OK)
def check_precond(op_precond, params):
    match op_precond.operand:
        case 'at':
            type1 = op_precond.object_types[0]
            obj1 = find_with_variable(params, type1)
            type2 = op_precond.object_types[1]
            obj2 = find_with_variable(params, type2)
            if obj1.value.location == None:
                return False
            elif obj1.value.location.name != obj2.value.name:
                return False
            else:
                return True
        case 'in':
            type1 = op_precond.object_types[0]
            obj1 = find_with_variable(params, type1)
            type2 = op_precond.object_types[1]
            obj2 = find_with_variable(params, type2)
            if not obj1.value in obj2.value.cargo:
                return False
            else:
                return True
        case 'has-fuel':
            type1 = op_precond.object_types[0]
            obj1 = find_with_variable(params, type1)
            if not obj1.value.has_fuel:
                return False
            else:
                return True