from FactLayer import apply_effects

def extract_plan(fact_graph, action_graph, goals):
    plan = []

    for action, params in action_graph[-1]:
        result_list = []
        found = apply_effects(action, params, fact_graph[-2], result_list)
        for cargo, destination in goals:
            for result in result_list:
                if result.name == cargo.name and result.location.name == destination.name:
                    print(found[0].location.name)



    return plan