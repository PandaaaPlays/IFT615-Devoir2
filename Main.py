import argparse
import re
from audioop import reverse

import ActionLayer
from ActionLayer import create_action_layer, ROCKET, CARGO, PLACE
from ExtractPlan import extract_plan
from FactLayer import create_fact_layer
from Objects import VariablePair, Operator, Parameter, Precondition, Effect
from Utils import find_in_list, read_lines

def check_params(op_params, params):
    if len(op_params) != len(params):
        raise ValueError("Le nombre de parametres donné n'est pas le bon selon le nombre d'opérateurs.")
    list = []

    for op_param, param in zip(op_params, params):
        if not isinstance(param, eval(op_param.type)):
            raise ValueError(f"Parametre {param.name} ne match pas le type attendu : {op_param.type}")
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
                facts.append(PLACE(name, None))
            case 'CARGO':
                facts.append(CARGO(name, None))
            case 'ROCKET':
                facts.append(ROCKET(name, None))
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

    return DoPlan(operators, facts)

def DoPlan(operators, facts):
    initial_state = facts
    fact_graph = [list(initial_state)]
    action_graph = []
    goals = [(fact, fact.destination) for fact in facts if isinstance(fact, CARGO) and fact.destination]

    plan = []
    mutex_actions = []
    i = 0

    while not goals_satisfied(goals, fact_graph[i]):
        print(f"\nIteration {i} :")

        print(f"Facts:")
        for fact in fact_graph[i]:
            print(f" - {fact.name}")
            if isinstance(fact, ActionLayer.OBJECT):
                print(f"   Location: {fact.location.name if fact.location else 'None'}")
            if isinstance(fact, ROCKET):
                print(f"   Has fuel: {fact.has_fuel}")
                print(f"   Cargos: {fact.cargo}")
                print(f"   Actions: ")
                if fact.action:
                    for action in fact.action:
                        print(f"    - {action}")
            if isinstance(fact, CARGO):
                print(f"   Destination: {fact.destination.name if fact.destination else 'None'}")
                print(f"   Actions: ")
                if fact.action:
                    for action in fact.action:
                        print(f"    - {action}")

        # Créer l'action layer
        action_layer, mutex_action = create_action_layer(fact_graph[i], operators)
        action_graph.append(action_layer)
        mutex_actions.append(mutex_action)

        # Créer la fact layer
        fact_layer = create_fact_layer(action_graph[-1], fact_graph[-1])
        fact_graph.append(fact_layer)

        i += 1

    # Extraire la solution
    goal_facts = set()
    for fact in fact_graph[-1]:
        if isinstance(fact, CARGO):
            if fact.location and fact.location.name == fact.destination.name:
                goal_facts.add(fact)
    plan = extract_plan(fact_graph, goal_facts)

    return plan


def goals_satisfied(goals, graph):
    cargo_dict = {cargo.name: False for cargo, destination in goals}

    for obj in graph:
        if isinstance(obj, ActionLayer.CARGO) and obj.destination == obj.location:
            cargo_dict[obj.name] = True

    return all(cargo_dict.values())


def main():
    parser = argparse.ArgumentParser(description='Planificateur de tâches utilisant l\'algorithme Graphplan')
    parser.add_argument('r_ops', type=str, help='Fichier contenant les opérateurs')
    parser.add_argument('r_facts', type=str, help='Fichier contenant les conditions initiales et les objectifs')

    args = parser.parse_args()

    optimal_plan = reversed(graphplan(args.r_ops, args.r_facts))
    print("Plan optimal:")
    for step in optimal_plan:
        print(step.operator.name)

if __name__ == "__main__":
    main()