def read_lines(file_path):
    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            lines.append(line)
    return lines


def find_in_list(fact_list, name):
    for fact in fact_list:
        if fact.name == name:
            return fact
    raise ValueError(f"{name} pas trouvé dans la liste")


def find_with_obj(fact_list, obj):
    for fact in fact_list:
        if fact == obj:
            return fact
    raise ValueError(f"{obj} pas trouvé dans la liste")


def find_with_variable(fact_list, variable):
    for fact in fact_list:
        if fact.variable.name == variable:
            return fact
    raise ValueError(f"{variable} pas trouvé dans la liste")
