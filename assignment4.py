from collections import defaultdict

neg = '~'

class dir_graph:
    def __init__(self):
        self.graph = defaultdict(set)
        self.nodes = set()

    def addEdge(self, u, v):
        self.graph[u].add(v)
        self.nodes.add(u)
        self.nodes.add(v)

class two_cnf:
    def __init__(self):
        self.con = []

    def add_clause(self, clause):
        if len(clause) <= 2:
            self.con.append(clause)
        else:
            print("Error: clause contains > 2 literals")

def double_neg(formula):
    return formula.replace((neg+neg), '')

def DFS(dir_graph, visited, stack, scc):
    for node in dir_graph.nodes:
        if node not in visited:
            explore(dir_graph, visited, node, stack, scc)

def explore(dir_graph, visited, node, stack, scc):
    if node not in visited:
        visited.append(node)
        for neighbour in dir_graph.graph[node]:
            explore(dir_graph, visited, neighbour, stack, scc)
        stack.append(node)
        scc.append(node)
    return visited

def transpose_graph(d_graph):
    t_graph = dir_graph()
    for node in d_graph.graph:
        for neighbour in d_graph.graph[node]:
            t_graph.addEdge(neighbour, node)
    return t_graph

def strongly_connected_components(dir_graph):
    stack = []
    sccs = []
    DFS(dir_graph, [], stack, [])
    t_g = transpose_graph(dir_graph)
    visited = []
    while stack:
        node = stack.pop()
        if node not in visited:
            scc = []
            scc.append(node)
            explore(t_g, visited, node, [], scc)
            sccs.append(scc)
    return sccs

def find_contradiction(sccs):
    for component in sccs:
        for literal in component:
            if double_neg(neg + literal) in component:
                return True
    return False

def two_sat_solver(two_cnf_formula):
    graph = dir_graph()
    for clause in two_cnf_formula.con:
        if len(clause) == 2:
            u, v = clause
            graph.addEdge(double_neg(neg+u), v)
            graph.addEdge(double_neg(neg+v), u)
        else:
            u = clause[0]
            graph.addEdge(double_neg(neg+u), u)
    sccs = strongly_connected_components(graph)
    return "yes" if not find_contradiction(sccs) else "no"

def can_turn_off_lights(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        instances = file.read().strip().split('***')[1:]

    results = []
    for instance in instances:
        if not instance.strip(): 
            continue
        lines = instance.strip().split('\n')
        n, m = map(int, lines[0].split(','))
        state = list(map(int, lines[1].split(',')))
        connections = [list(map(int, line.split(','))) for line in lines[2:]]

        formula = two_cnf()
        for light in range(1, m + 1):
            switches = [i + 1 for i, s in enumerate(connections) if light in s]
            if len(switches) == 2:
                s1, s2 = switches
                if state[light - 1] == 1:
                    # If the light is initially on, need to flip at least one switch to turn it off
                    formula.add_clause([f's{s1}', f's{s2}'])
                    formula.add_clause([f'~s{s1}', f'~s{s2}'])
                else:
                    # If the light is initially off, both switches must be flipped or not flipped to keep it off
                    formula.add_clause([f's{s1}', f'~s{s2}'])
                    formula.add_clause([f'~s{s1}', f's{s2}'])
            else:
                print("Error: A light is not connected to exactly two switches.")

        result = two_sat_solver(formula)
        print(result)
        results.append(result)

    with open(output_file_path, 'w') as file:
        for result in results:
            file.write(result + '\n')

input_file_path = '/Users/lianghui/Downloads/cs325_algorithm/samples_subset/test_small_2.txt'  
output_file_path = '/Users/lianghui/Downloads/cs325_algorithm/output.txt'  
can_turn_off_lights(input_file_path, output_file_path)
