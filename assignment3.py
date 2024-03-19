'''
    This file contains the template for Assignment3.  For testing it, I will place it
    in a different directory, call the function <minimum_cost_connectg_edges>, and check
    its output. So, you can add/remove  whatever you want to/from this file.  But, don't
    change the name of the file or the name/signature of the following function.

    Also, I will use <python3> to run this code.
'''

import re

def minimum_cost_connectg_edges(input_file_path, output_file_path):

    with open(input_file_path, 'r') as file:
        input_line1 = file.readline().strip()
        # P = [tuple(map(int, point.split(','))) for point in file.readline().strip().split()]
        # points = re.findall(r'\((-?\d+), (-?\d+)\)', input_line1)
        points = re.findall(r'\((-?\d+)\s*,\s*(-?\d+)\)', input_line1)
        P = [tuple(map(int, match))for match in points]
        input_line2 = file.readline().strip()
        # edges = re.findall(r'\((-?\d+), (-?\d+)\)', input_line2)
        edges = re.findall(r'\((-?\d+)\s*,\s*(-?\d+)\)', input_line2)
        if edges != "none":
            E1 = [tuple(map(int, match))for match in edges]
        else:
            E1 = []

    # print (P, E1)
    
    union_find = UnionFind(len(P))

    for e1, e2 in E1:
        union_find.union(e1-1, e2-1)

    E_star = []
    for i in range(len(P)):
        for j in range(i+1, len(P)):
            if (i+1, j+1) not in E1 and (j+1, i+1) not in E1:
                weight = manhatan_distance(P[i], P[j])
                E_star.append((weight, i, j))

    E_star.sort()

    mst = 0
    for weight, e1, e2 in E_star:
        if union_find.find(e1) != union_find.find(e2):
            union_find.union(e1, e2)
            mst += weight

    with open(output_file_path, 'w') as file:
        file.write(str(mst))
            
def manhatan_distance(p1, p2):
    d = abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])
    return d

class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, e1):
        if self.parent[e1] != e1:
            self.parent[e1] = self.find(self.parent[e1])
        return self.parent[e1]

    def union(self, e1, e2):
        roote1 = self.find(e1)
        roote2 = self.find(e2)
        if roote2 != roote1:
            if self.rank[roote2] > self.rank[roote1]:
                self.parent[roote1] = roote2
            elif self.rank[roote2] < self.rank[roote1]:
                self.parent[roote2] = roote1
            else:
                self.parent[roote1] = roote2
                self.rank[roote2] += 1

input_file_path = '/Users/lianghui/Downloads/cs325_algorithm/ga3-all-test-cases/input17.in'
output_file_path = '/Users/lianghui/Downloads/cs325_algorithm/output.txt'
minimum_cost_connectg_edges(input_file_path, output_file_path)

