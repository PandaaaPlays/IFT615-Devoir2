from itertools import product

from Objects import VariablePair, Fact
from Utils import find_with_variable

class PLACE(Fact):
    def __init__(self, name):
        super().__init__(name)


class OBJECT(Fact):
    def __init__(self, name):
        super().__init__(name)
        self.location = []

    def add_location(self, location):
        self.location.append(location)

    def remove_location(self, location):
        self.location.remove(location)


class CARGO(OBJECT):
    def __init__(self, name):
        super().__init__(name)
        self.destination = None

    def set_destination(self, destination):
        self.destination = destination


class ROCKET(OBJECT):
    def __init__(self, name):
        super().__init__(name)
        self.has_fuel = False
        self.cargo = []

    def set_has_fuel(self, has_fuel):
        self.has_fuel = has_fuel

    def add_cargo(self, cargo):
        self.cargo.append(cargo)

    def remove_cargo(self, cargo):
        self.cargo.remove(cargo)


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
            if obj1.value.location[0].name != obj2.value.name:
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