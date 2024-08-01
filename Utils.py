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
    raise ValueError(f"{name} not found in the list")


def find_with_variable(fact_list, variable):
    for fact in fact_list:
        if fact.variable.name == variable:
            return fact
    raise ValueError(f"{variable} not found in the list")
