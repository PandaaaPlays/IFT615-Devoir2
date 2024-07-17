import argparse


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

class ROCKET(OBJECT):
    def __init__(self, name):
        super().__init__(name)
        self.has_fuel = None
    def set_has_fuel(self, has_fuel):
        self.has_fuel = has_fuel
def read_lines(file_path):
    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            lines.append(line)
    return lines


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
                facts.append(OBJECT(name))
            case 'ROCKET':
                facts.append(ROCKET(name))
        print(facts[counter].name)
        counter += 1


    # Print the lines read for demonstration purposes
    print("Operators:", file_operators)
    print("Facts:", file_facts)

    # Implement your Graphplan logic here

    # Example of an optimal plan (empty for now)
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