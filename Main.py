import argparse
import re
from itertools import product

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
        self.cargo = []
    def set_has_fuel(self, has_fuel):
        self.has_fuel = has_fuel
    def add_cargo(self, cargo):
        self.cargo.append(cargo)
    def remove_cargo(self, cargo):
        self.cargo.remove(cargo)


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
def apply_effect(op_effect, param_dict, facts):
    match op_effect.operand:
        case 'in':
            type1 = op_effect.object_types[0].strip('()')
            obj1 = param_dict[type1]
            type2 = op_effect.object_types[1].strip('()')
            obj2 = param_dict[type2]
            find_in_list(facts, obj2.name).add_cargo(obj1)
        case 'del':
            match op_effect.object_types[0]:
                case 'at':
                    type1 = op_effect.object_types[1].strip('()')
                    obj1 = param_dict[type1]
                    type2 = op_effect.object_types[2].strip('()')
                    obj2 = param_dict[type2]
                    if obj1.location.name == obj2.name:
                        find_in_list(facts, obj1.name).set_location(None)
                case 'in':
                    type1 = op_effect.object_types[2].strip('()')
                    obj1 = param_dict[type1]
                    type2 = op_effect.object_types[1].strip('()')
                    obj2 = param_dict[type2]
                    find_in_list(facts, obj1.name).remove_cargo(obj2)
                case 'has-fuel':
                    type1 = op_effect.object_types[1].strip('()')
                    obj1 = param_dict[type1]
                    find_in_list(facts, obj1.name).set_has_fuel(False)
        case 'at':
            type1 = op_effect.object_types[0].strip('()')
            obj1 = param_dict[type1]
            type2 = op_effect.object_types[1].strip('()')
            obj2 = param_dict[type2]
            find_in_list(facts, obj1.name).set_location(obj2)


def handle_operation(operator, params, facts):
    params_list = check_params(operator.params, params)
    for precond in operator.preconds:
        check_precond(precond, params_list)
    for effect in operator.effects:
        apply_effect(effect, params_list, facts)


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

    return DoPlan(operators, facts)

def DoPlan(operators, facts):
    # Implement the Graphplan algorithm to find the optimal plan
    # 1. Initialize the planning graph with initial facts
    # 2. Expand the graph by alternating between action and fact layers
    # 3. Check for goal reachability and extract the plan

    initial_state = set(facts)
    # Create a list of goals as (cargo, destination) tuples
    goals = [(fact, fact.destination) for fact in facts if isinstance(fact, CARGO) and fact.destination]

    plan = []
    planning_graph = []
    planning_graph.append(initial_state)

    # While goals are not satisfied
    while not goals_satisfied(goals):
        print("New iteration!")
        # Create action layer
        print("Creating action layer!")
        action_layer = create_action_layer(planning_graph[-1], operators)
        planning_graph.append(action_layer)

        # Create fact layer
        print("Creating fact layer!")
        fact_layer = create_fact_layer(action_layer)
        planning_graph.append(fact_layer)
        print("Planning_graph: ", planning_graph)

    # Extract plan from the planning graph
    plan = extract_plan(planning_graph, goals, operators)
    return plan

def goals_satisfied(goals):
    # Check if all goals are satisfied in the current state
    for cargo, destination in goals:
        if cargo.location != destination:
            return False
    return True

def create_action_layer(state, operators):
    action_layer = []
    for operator in operators:
        # Generate all possible combinations of parameters for the operator
        possible_params = [
            [fact for fact in state if isinstance(fact, eval(param.type))]
            for param in operator.params
        ]
        # Check each combination of parameters
        for param_combination in product(*possible_params):

            param_dict = {param.name: fact for param, fact in zip(operator.params, param_combination)}
            if preconditions_satisfied(operator, param_dict):
                action_layer.append((operator, param_dict))
    #for action in action_layer:
        #print("new action")
        #print("operator: ", action[0].name)
        #print("params: ", action[1])
    return action_layer

def preconditions_satisfied(operator, param_dict):
    # Create a list of VariablePairs from the param_dict
    params_list = [VariablePair(param, param_dict[param.name]) for param in operator.params]

    for precond in operator.preconds:
        if not check_precond(precond, params_list):
            return False
    return True

def create_fact_layer(action_layer):
    # Create a fact layer based on the action layer
    fact_layer = set()
    for action, param_dict in action_layer:
        for effect in action.effects:
            apply_effect(effect, param_dict, fact_layer)
    return fact_layer

def extract_plan(planning_graph, goals, operators):
    # Extract a plan from the planning graph by backtracking from the goals
    plan = []
    for i in range(len(planning_graph) - 1, 0, -2):
        action_layer = planning_graph[i - 1]
        fact_layer = planning_graph[i]

        for goal in goals:
            for action in action_layer:
                if any(effect.operand == 'at' and effect.object_types[0].strip('()') == goal[0].name and
                       effect.object_types[1].strip('()') == goal[1].name for effect in action.effects):
                    plan.append(action)
                    break
    return plan

def main():
    parser = argparse.ArgumentParser(description='Planificateur de tâches utilisant l\'algorithme Graphplan')
    parser.add_argument('r_ops', type=str, help='Fichier contenant les opérateurs')
    parser.add_argument('r_facts', type=str, help='Fichier contenant les conditions initiales et les objectifs')

    args = parser.parse_args()

    optimal_plan = graphplan(args.r_ops, args.r_facts)
    print("Optimal Plan:")
    for step in optimal_plan:
        print(step.name)

if __name__ == "__main__":
    main()