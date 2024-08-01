class Fact:
    def __init__(self, name):
        self.name = name


class Operator:
    def __init__(self, name):
        self.name = name
        self.params = []
        self.preconds = []
        self.effects = []

    def add_param(self, param):
        self.params.append(param)

    def add_precond(self, precond):
        self.preconds.append(precond)

    def add_effect(self, effect):
        self.effects.append(effect)


class Parameter:
    def __init__(self, name, type):
        self.name = name
        self.type = type


class Precondition:
    def __init__(self, operand, object_types):
        self.operand = operand
        self.object_types = object_types


class Effect:
    def __init__(self, operand, object_types):
        self.operand = operand
        self.object_types = object_types


class VariablePair:
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value
