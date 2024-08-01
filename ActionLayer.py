from itertools import product

from Objects import VariablePair, Fact
from Utils import find_with_variable

class PLACE(Fact):
    def __init__(self, name):
        super().__init__(name)


class OBJECT(Fact):
    def __init__(self, name):
        super().__init__(name)
        self.location = None

    def set_location(self, location):
        self.location = location


class CARGO(OBJECT):
    def __init__(self, name):
        super().__init__(name)
        self.destination = None

    def set_destination(self, destination):
        self.destination = destination

    def __copy__(self):
        new_cargo = CARGO(self.name)
        new_cargo.destination = self.destination
        new_cargo.location = self.location
        return new_cargo


class ROCKET(OBJECT):
    def __init__(self, name):
        super().__init__(name)
        self.has_fuel = False
        self.cargo = set()

    def set_has_fuel(self, has_fuel):
        self.has_fuel = has_fuel

    def add_cargo(self, cargo):
        self.cargo.add(cargo)

    def remove_cargo(self, cargo):
        self.cargo.discard(cargo)

    def __copy__(self):
        new_rocket = ROCKET(self.name)
        new_rocket.cargo = self.cargo
        new_rocket.set_location(self.location)
        new_rocket.set_has_fuel(self.has_fuel)
        return new_rocket


def create_action_layer(fact_layer, operators):
    action_layer = []
    for operator in operators:
        possible_params = [
            [fact for fact in fact_layer if isinstance(fact, eval(param.type))]
            for param in operator.params
        ]
        for param_combination in product(*possible_params):
            param_dict = {param.name: fact for param, fact in zip(operator.params, param_combination)}
            if preconditions_satisfied(operator, param_dict):
                action_layer.append((operator, param_dict))
    return action_layer


def preconditions_satisfied(operator, param_dict):
    # Create a list of VariablePairs from the param_dict
    params_list = [VariablePair(param, param_dict[param.name]) for param in operator.params]

    for precond in operator.preconds:
        if not check_precond(precond, params_list):
            return False
    return True


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