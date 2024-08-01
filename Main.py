import argparse
import re

import ActionLayer
from ActionLayer import create_action_layer, ROCKET, CARGO, PLACE
from FactLayer import create_fact_layer
from Objects import VariablePair, Operator, Parameter, Precondition, Effect
from Utils import find_with_variable, find_in_list, read_lines

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
        counter += 1;
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
    initial_state = facts
    planning_graph = [list(initial_state)]
    goals = [(fact, fact.destination) for fact in facts if isinstance(fact, CARGO) and fact.destination]

    plan = []
    no_solution = False
    i = 0

    # 2. Expand the graph by alternating between action and fact layers
    while not goals_satisfied(goals, planning_graph[i]):
        print(f"\nIteration {i} :")

        print(f"Facts:")
        for fact in planning_graph[i]:
            print(f" - {fact.name}")
            if isinstance(fact, ActionLayer.OBJECT):
                print(f"   Location: {fact.location.name if fact.location else 'None'}")
            if isinstance(fact, ROCKET):
                print(f"   Has fuel: {fact.has_fuel}")
                print(f"   Cargos: {fact.cargo}")
            if isinstance(fact, CARGO):
                print(f"   Destination: {fact.destination.name if fact.destination else 'None'}")

        # Printing actual facts
        # print(f"Facts:")
        # for fact in planning_graph[i]:
        #    print(f" - {fact.name}")

        # Create action layer
        action_layer = create_action_layer(planning_graph[i], operators)

        # Printing actions
        # for action, params in action_layer:
        #    print(f"Action: {action.name}")
        #    for param_name, fact in params.items():
        #        print(f"  {param_name}: {fact.name} (Type: {type(fact).__name__})")

        # Create fact layer
        fact_layer = create_fact_layer(action_layer, planning_graph[i])
        planning_graph.append(fact_layer)

        i += 1

    # 3. Check for goal reachability and extract the plan
    #plan = extract_plan(planning_graph, goals, operators)
    return plan


def goals_satisfied(goals, graph):
    cargo_dict = {cargo.name: False for cargo, destination in goals}

    for obj in graph:
        if isinstance(obj, ActionLayer.CARGO) and obj.destination == obj.location:
            cargo_dict[obj.name] = True

    #print(cargo_dict)

    return all(cargo_dict.values())


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