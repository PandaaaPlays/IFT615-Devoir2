import ActionLayer
from Utils import find_with_obj


def extract_plan(fact_graph, goal_facts):
    plan = []

    print("\n==================================")
    print("Extraire le plan optimal: ")
    print("==================================")

    print("Facts (goals) de la derniere iteration: ")
    for fact in goal_facts:
        print(f" - {fact.name}")
        if isinstance(fact, ActionLayer.OBJECT):
            print(f"   Location: {fact.location.name if fact.location else 'None'}")
        if isinstance(fact, ActionLayer.ROCKET):
            print(f"   Has fuel: {fact.has_fuel}")
            print(f"   Cargos: {fact.cargo}")
            print(f"   Actions menant a cette rocket: ")
            if fact.action:
                for action in fact.action:
                    print(f"    - {action}")
        if isinstance(fact, ActionLayer.CARGO):
            print(f"   Destination: {fact.destination.name if fact.destination else 'None'}")
            print(f"   Actions menant a ce cargo: ")
            if fact.action:
                for action in fact.action:
                    print(f"    - {action}")

    new_goals = set()
    for goal in goal_facts:
        for action in goal.action:
            params = action.params
            #print(f"Action : {action} ({action.operator.name})")
            for effect in action.operator.effects:
                #print(f" - Effect : {effect.operand}")
                for type in effect.object_types:
                    type = type.strip("()")
                    if type == "<rocket>" or type == "<object>" or type == "<to>" or type == "<from>":
                        obj = params[type]
                        #print(f"   - Type : {type} ({find_with_obj(fact_graph[-2], obj)})")
                        add(action, plan)
                        new_goals.add(find_with_obj(fact_graph[-2], obj))


    print(new_goals)
    for fact in new_goals:
        print(f" - {fact.name}")
        if isinstance(fact, ActionLayer.OBJECT):
            print(f"   Location: {fact.location.name if fact.location else 'None'}")
        if isinstance(fact, ActionLayer.ROCKET):
            print(f"   Has fuel: {fact.has_fuel}")
            print(f"   Cargos: {fact.cargo}")
            print(f"   Actions menant a cette rocket: ")
            if fact.action:
                for action in fact.action:
                    print(f"    - {action}")
        if isinstance(fact, ActionLayer.CARGO):
            print(f"   Destination: {fact.destination.name if fact.destination else 'None'}")
            print(f"   Actions menant a ce cargo: ")
            if fact.action:
                for action in fact.action:
                    print(f"    - {action}")


    new_goals2 = set()
    for goal in new_goals:
        for action in goal.action:
            params = action.params
            for effect in action.operator.effects:
                for type in effect.object_types:
                    type = type.strip("()")
                    if type == "<rocket>" or type == "<object>" or type == "<to>" or type == "<from>":
                        obj = params[type]
                       # print(f"   - Type : {type} ({find_with_obj(fact_graph[-3], obj)})")
                        add(action, plan)
                        new_goals2.add(find_with_obj(fact_graph[-3], obj))

    print(new_goals2)
    for fact in new_goals2:
        print(f" - {fact.name}")
        if isinstance(fact, ActionLayer.OBJECT):
            print(f"   Location: {fact.location.name if fact.location else 'None'}")
        if isinstance(fact, ActionLayer.ROCKET):
            print(f"   Has fuel: {fact.has_fuel}")
            print(f"   Cargos: {fact.cargo}")
            print(f"   Actions menant a cette rocket: ")
            if fact.action:
                for action in fact.action:
                    print(f"    - {action}")
        if isinstance(fact, ActionLayer.CARGO):
            print(f"   Destination: {fact.destination.name if fact.destination else 'None'}")
            print(f"   Actions menant a ce cargo: ")
            if fact.action:
                for action in fact.action:
                    print(f"    - {action}")

    return plan

def add(action, plan):
    contains = False
    for actions in plan:
        if action == actions:
            contains = True

    if not contains:
        plan.append(action)