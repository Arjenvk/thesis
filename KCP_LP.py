### Python function to solve the KCP with linear programming
### Input: Graph, k, max lengths
### Output: A minimum K centre location(s) of G

import pulp
import networkx as nx
import math

def create_Graph_KCP(points, max_length):
    G = nx.DiGraph()
    # add nodes
    k = 1
    G.add_node(k, pos=(points[k-1]))
    print("node", k, "added. coordinates: ", points[k-1])
    while len(list(G)) < len(points):
        k += 1
        G.add_node(k, pos=(points[k-1]))
        print("node", k, "added. coordinates: ", points[k-1])

    # add edges, if length is more than max_length then add artificial high weight
    seen_edge = set()
    for k in range(1, len(points)+1):
        for l in range(1, len(points)+1):
            if k == l:
                G.add_edge(k, l, weight=999) # artificially high weight
                seen_edge.add((k,l))
                print("edge", k, "to", l, "added with weight 999")
            else:
                length = math.sqrt((points[k-1][0] - points[l-1][0])**2 + (points[k-1][1] - points[l-1][1])**2)
                if length < max_length:
                    G.add_edge(k, l, weight=length)
                    seen_edge.add((k,l))
                    print("edge", k, "to", l, "added with weight", length)
                else:
                    G.add_edge(k, l, weight=999) # artificially high weight
                    seen_edge.add((k,l))
                    print("edge", k, "to", l, "added with weight 999")
    return G

def KCP_LP(Graph, K):
    y = pulp.LpVariable.dicts("y", Graph.nodes(), cat=pulp.LpBinary)
    #print(y)
    x = pulp.LpVariable.dicts("x", Graph.edges(), cat=pulp.LpBinary)
    # print(x)
    z = pulp.LpVariable("z", cat=pulp.LpContinuous)

    ## make optimisation problem
    prob = pulp.LpProblem("K-centreProblem", pulp.LpMinimize)

    ## add objective function
    prob += z

    ## add the first constraint set
    # Z is greater or equal to the weights of the edges in the solution
    for l in range(1,len(points)+1):
        for k in range(1,len(points)+1):
            print(' constraint of edge', l, 'to', k, 'is added with a length of:', Graph.edges[l,k]['weight'])
            prob += Graph.edges[l,k]['weight'] * x[l,k] <= z


    ## add the second constraint set
    # every node is connected to at least one node in the solution
    for l in range(1,len(points)+1):
        prob += pulp.lpSum([x[l,k] for k in Graph.nodes()]) == 1

    ## add the third constraint set
    # nodes can only be connected to a node in the solution set
    for l in range(1,len(points)+1):
        for k in range(1,len(points)+1):
            if Graph.has_edge(l,k) == True:
                prob += x[l,k] <= y[k]


    ## add the fourth constraint set
    # the number of nodes in the solution set is equal to K
    prob += pulp.lpSum([y[l] for l in Graph.nodes()]) <= K

    ## solve the problem
    prob.solve()

    ## print the results
    print("Status:", pulp.LpStatus[prob.status])
    print("maximum edge distance is:", pulp.value(prob.objective))
    for v in prob.variables():
        if v.varValue == 1.0:
            print('node', v.name, "is in dominating Set")

points = [[1, 8], [6, 3], [5,6], [5, 8], [9, 1], [4,9], [8,9], [3,1]]
max_length = 6
K = 2

Graph = create_Graph_KCP(points, max_length)
KCP_LP(Graph, K)