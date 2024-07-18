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

def find_fact(list, name):
    for fact in list:
        if fact.name == name:
            return fact

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
            object = find_fact(facts, parts[1])
            place = find_fact(facts, parts[2].strip('()'))
            object.set_location(place)
        if(argument == 'has-fuel'):
            rocket = find_fact(facts, parts[1].strip('()'))
            rocket.set_has_fuel(True)
        counter +=1

    counter += 1

    while counter < len(file_facts):
        print(file_facts[counter])
        parts = file_facts[counter].split()
        cargo = find_fact(facts, parts[1].strip('()'))
        place = find_fact(facts, parts[2].strip('()'))
        cargo.set_destination(place)
        counter += 1

    print("Operators:", file_operators)
    print("Facts:")
    for fact in facts:
        print("Name: " + fact.name)
        if isinstance(fact, OBJECT):
            print("Location: " + fact.location.name)
        if isinstance(fact, ROCKET):
            print("Has fuel: " + str(fact.has_fuel))
        if isinstance(fact, CARGO):
            print("Destination: " + fact.destination.name)


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