import argparse
import re

class Fact:
    def __init__(self, name):
        self.name = name

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

class ROCKET(OBJECT):
    def __init__(self, name):
        super().__init__(name)
        self.has_fuel = False
        self.cargo = None
    def set_has_fuel(self, has_fuel):
        self.has_fuel = has_fuel
    def set_cargo(self, cargo):
        self.cargo = cargo

class Operator:
    def __init__(self, name):
        self.name = name
        self.params = []
        self.preconds = []
        self.effects =[]

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

def read_lines(file_path):
    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            lines.append(line)
    return lines

def find_in_list(list, name):
    for fact in list:
        if fact.name == name:
            return fact
    raise ValueError(f"{name} not found in the list")

def get_class_by_name(name):
    return globals()[name]

def find_with_type(list, type_str):
    type_class = get_class_by_name(type_str.upper())
    for fact in list:
        if isinstance(fact, type_class):
            return fact
    raise ValueError(f"{type_str} not found in the list")
def find_with_variable(list, variable):
    for var in list:
        if var.variable.name == variable:
            return var
    raise ValueError(f"{variable} not found in the list")


def check_params(op_params, params):
    if len(op_params) != len(params):
        raise ValueError("Number of parameters given do not match the number of operator parameters")
    list = []

    for op_param, param in zip(op_params, params):
        if not isinstance(param, eval(op_param.type)):
            raise ValueError(f"Parameter {param.name} does not match the expected type {op_param.type}")
        else:
            list.append(VariablePair(op_param, param))

    return list

def check_precond(op_precond, params):
    match op_precond.operand:
        case 'at':
            type1 = op_precond.object_types[0]
            obj1 = find_with_variable(params, type1)
            type2 = op_precond.object_types[1]
            obj2 = find_with_variable(params, type2)
            if obj1.value.location.name != obj2.value.name:
                raise ValueError(f"Object {obj1.name} is not at the location {obj2.name}")
            else:
                return True
        case 'in':
            type1 = op_precond.object_types[0]
            obj1 = find_with_variable(params, type1)
            type2 = op_precond.object_types[1]
            obj2 = find_with_variable(params, type2)
            if obj2.value.cargo.name != obj1.value.name:
                raise ValueError(f"Object {obj1.name} is not in the rocket {obj2.name}")
            else:
                return True
        case 'has-fuel':
            type1 = op_precond.object_types[0]
            obj1 = find_with_variable(params, type1)
            if not obj1.value.has_fuel:
                raise ValueError(f"Object {obj1.name} has no fuel")
            else:
                return True
def apply_effect(op_effect, params, facts):
    match op_effect.operand:
        case '(in':
            type1 = op_effect.object_types[0].strip('()')
            obj1 = find_with_variable(params, type1)
            type2 = op_effect.object_types[1].strip('()')
            obj2 = find_with_variable(params, type2)
            find_in_list(facts, obj2.value.name).set_cargo(obj1.value)
        case '(del':
            match op_effect.object_types[0]:
                case 'at':
                    type1 = op_effect.object_types[1].strip('()')
                    obj1 = find_with_variable(params, type1)
                    type2 = op_effect.object_types[2].strip('()')
                    obj2 = find_with_variable(params, type2)
                    if(obj1.value.location.name == obj2.value.name):
                        find_in_list(facts, obj1.value.name).set_location(None)
                case 'in':
                    type1 = op_effect.object_types[2].strip('()')
                    obj1 = find_with_variable(params, type1)
                    find_in_list(facts, obj1.value.name).set_cargo(None)
                case 'has-fuel':
                    type1 = op_effect.object_types[1].strip('()')
                    obj1 = find_with_variable(params, type1)
                    find_in_list(facts, obj1.value.name).set_has_fuel(False)
        case '(at':
            type1 = op_effect.object_types[0].strip('()')
            obj1 = find_with_variable(params, type1)
            type2 = op_effect.object_types[1].strip('()')
            obj2 = find_with_variable(params, type2)
            find_in_list(facts, obj1.value.name).set_location(obj2.value)
            print("we have set the location of " + obj1.value.name + " to " + obj2.value.name)


def handle_operation(operator, params, facts):
    params_list = check_params(operator.params, params)
    for precond in operator.preconds:
        check_precond(precond, params_list)
    for effect in operator.effects:
        apply_effect(effect, params_list, facts)
    print("We made it here!")


def graphplan(r_ops_file, r_facts_file):
    # Read all lines from each file until an empty line or EOF is encountered
    file_operators = read_lines(r_ops_file)
    file_facts = read_lines(r_facts_file)

    facts = []
    counter = 0
    while file_facts[counter].split()[0] != '(preconds':
        parts = file_facts[counter].split()
        name = parts[0].strip('()')
        fact_type = parts[1].strip('()')
        match fact_type:
            case 'PLACE':
                facts.append(PLACE(name))
            case 'CARGO':
                facts.append(CARGO(name))
            case 'ROCKET':
                facts.append(ROCKET(name))
        counter += 1

    counter +=1

    while file_facts[counter].split()[0] != '(effects':
        parts = file_facts[counter].split()
        argument = parts[0].strip('()')
        if(argument == 'at'):
            object = find_in_list(facts, parts[1])
            place = find_in_list(facts, parts[2].strip('()'))
            object.set_location(place)
        if(argument == 'has-fuel'):
            rocket = find_in_list(facts, parts[1].strip('()'))
            rocket.set_has_fuel(True)
        counter += 1

    counter += 1

    while counter < len(file_facts):
        parts = file_facts[counter].split()
        cargo = find_in_list(facts, parts[1].strip('()'))
        place = find_in_list(facts, parts[2].strip('()'))
        cargo.set_destination(place)
        counter += 1

    counter = 0
    operators = []
    while counter < len(file_operators):
        counter += 1; #skip la ligne operator
        op = Operator(file_operators[counter])
        counter += 2
        parts = re.findall(r'\([^)]*\)', file_operators[counter])
        for args in parts:
            arg_name = args.split()[0].strip('()')
            arg_type = args.split()[1].strip('()')
            param = Parameter(arg_name, arg_type)
            op.add_param(param)
        counter += 2
        parts = re.findall(r'\([^)]*\)', file_operators[counter])
        for args in parts:
            split = args.split()
            operator = None
            arguments = []
            arg_counter = 0
            for arg in split:
                if arg_counter == 0:
                    operator = arg.strip('()')
                else:
                    arguments.append(arg.strip('()'))
                arg_counter += 1
            op.add_precond(Precondition(operator, arguments))
        counter += 2
        parts = re.findall(r'\([^)]*\)', file_operators[counter])
        for args in parts:
            split = args.split()
            operator = None
            arguments = []
            arg_counter = 0
            for arg in split:
                if arg_counter == 0:
                    operator = arg
                else:
                    arguments.append(arg)
                arg_counter += 1
            op.add_effect(Effect(operator, arguments))
        counter += 1
        operators.append(op)



    #print("Facts:")
    #for fact in facts:
     #   print("Name: " + fact.name)
      #  if isinstance(fact, OBJECT):
       #     print("Location: " + fact.location.name)
        #if isinstance(fact, ROCKET):
         #   print("Has fuel: " + str(fact.has_fuel))
        #if isinstance(fact, CARGO):
         #   print("Destination: " + fact.destination.name)

    params_list = [find_in_list(facts, 'alex'), find_in_list(facts, 'r1'), find_in_list(facts, 'London')]
    handle_operation(find_in_list(operators, 'LOAD'), params_list, facts)
    print(params_list[1].cargo.name)
    print(params_list[0].location)
    handle_operation(find_in_list(operators, 'UNLOAD'), params_list, facts)
    print(params_list[0].location.name)
    print(params_list[1].cargo)
    handle_operation(find_in_list(operators, 'LOAD'), params_list, facts)
    params_list = [find_in_list(facts, 'r1'), find_in_list(facts, 'London'), find_in_list(facts, 'Paris')]
    handle_operation(find_in_list(operators, 'MOVE'), params_list, facts)
    print(params_list[0].location.name)
    print(params_list[0].cargo.name)
    print(params_list[0].cargo.location)
    params_list = [find_in_list(facts, 'alex'), find_in_list(facts, 'r1'), find_in_list(facts, 'Paris')]
    handle_operation(find_in_list(operators, 'UNLOAD'), params_list, facts)
    print(params_list[0].location.name)
    optimal_plan = []
    return optimal_plan

def main():
    parser = argparse.ArgumentParser(description='Planificateur de tâches utilisant l\'algorithme Graphplan')
    parser.add_argument('r_ops', type=str, help='Fichier contenant les opérateurs')
    parser.add_argument('r_facts', type=str, help='Fichier contenant les conditions initiales et les objectifs')

    args = parser.parse_args()

    optimal_plan = graphplan(args.r_ops, args.r_facts)

if __name__ == "__main__":
    main()