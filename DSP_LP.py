### Python function to solve the DSP with linear programming
### Input: G, max lengths
### Output: A minimum dominating set of G

import pulp
import networkx as nx
import math

def create_Graph(points, max_length):
    G = nx.Graph()
    # add nodes
    k = 1
    G.add_node(k, pos=(points[k-1]))
    print("node", k, "added. coordinates: ", points[k-1])
    while len(list(G)) < len(points):
        k += 1
        G.add_node(k, pos=(points[k-1]))
        print("node", k, "added. coordinates: ", points[k-1])

    # add edges, if length is less than max_length
    seen_edge = set()
    for k in range(1, len(points)+1):
        for l in range(1, len(points)+1):
            if k != l:
                length = math.sqrt((points[k-1][0] - points[l-1][0])**2 + (points[k-1][1] - points[l-1][1])**2)
                if length < max_length:
                    # check if reverse arc is already in set
                    if (l,k) not in seen_edge and (k,l) not in seen_edge:
                        G.add_edge(k, l)
                        seen_edge.add((k,l))
                        print("edge", k, "to", l, "added")
    return G


def DSP_LP(Graph):
    y = pulp.LpVariable.dicts("y", Graph.nodes(), cat=pulp.LpBinary)
    prob = pulp.LpProblem("MinimumDominatingSet", pulp.LpMinimize)
    prob += pulp.lpSum(y)
    for v in Graph.nodes():
        prob += y[v] + pulp.lpSum([y[u] for u in Graph.neighbors(v)]) >= 1
    prob.solve()
    print("Status:", pulp.LpStatus[prob.status])
    print("Minimum dominating set size:", pulp.value(prob.objective))
    for v in prob.variables():
        if v.varValue == 1.0:
            print('node', v.name, "is in dominating Set")

points = [[1, 8], [6, 3], [5,6], [5, 8], [9, 1], [4,9], [8,9], [3,1]]
max_length = 6

Graph = create_Graph(points, max_length)
DSP_LP(Graph)