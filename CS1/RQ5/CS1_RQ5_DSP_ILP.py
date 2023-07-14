### Python function to solve the DSP with linear programming
### Input: G, max lengths
### Output: A minimum dominating set of G

import pulp
import networkx as nx
import math
import matplotlib.pyplot as plt


def create_Graph_DSP(points, max_length):
    G = nx.Graph()
    # add nodes
    k = 1
    G.add_node(k, pos=(points[k-1]))
    # print("node", k, "added. coordinates: ", points[k-1])
    while len(list(G)) < len(points):
        k += 1
        G.add_node(k, pos=(points[k-1]))
        # print("node", k, "added. coordinates: ", points[k-1])

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
                        # print("edge", k, "to", l, "added")
    return G
def DSP_LP(Graph1, Graph2, k, l):
    x = pulp.LpVariable.dicts("x", Graph1.nodes(), cat=pulp.LpBinary)
    y = pulp.LpVariable.dicts("y", Graph2.nodes(), cat=pulp.LpBinary)

    prob = pulp.LpProblem("MinimumDominatingSet", pulp.LpMinimize)

    prob += pulp.lpSum(y[i] + x[i] for i in Graph1.nodes())  # objective function

    ## constraints
    # Constraint 1: 
    for i in Graph1.nodes():
        prob += x[i] + pulp.lpSum([x[j] for j in Graph1.neighbors(i)]) + y[i] + pulp.lpSum([y[j] for j in Graph2.neighbors(i)]) >= 1

    # Constraint 2: 
    prob += pulp.lpSum([x[i] for i in Graph1.nodes()]) <= k
    prob += pulp.lpSum([y[i] for i in Graph2.nodes()]) <= l


    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    """
    # print results
    print("Status:", pulp.LpStatus[prob.status])
    for v in prob.variables():
        print(v.name, "=", v.varValue)
        print("Objective value:", pulp.value(prob.objective))
    """


    # return if feasible or not
    if prob.status == 1:
        return True
    else:
        return False
    
def create_graph_KCP(points):
    G = nx.DiGraph()
    # add nodes
    k = 1
    G.add_node(k, pos=(points[k-1]))
    # print("node", k, "added. coordinates: ", points[k-1])
    while len(list(G)) < len(points):
        k += 1
        G.add_node(k, pos=(points[k-1]))
        # print("node", k, "added. coordinates: ", points[k-1])

    # add edges to make a complete graph
    for k in range(1, len(points)+1):
        for l in range(1, len(points)+1):
            if k == l:
                G.add_edge(k, l, weight=0)
                # print("edge", k, "to", l, "added with weight", 999)
            elif k != l:
                length = math.sqrt((points[k-1][0] - points[l-1][0])**2 + (points[k-1][1] - points[l-1][1])**2)
                G.add_edge(k, l, weight=length)
                # print("edge", k, "to", l, "added with weight", length)
    return G
def KCP_Multi_LP(Graph1, Graph2, k):
    y1 = pulp.LpVariable.dicts("y1", Graph1.nodes(), cat=pulp.LpBinary)
    y2 = pulp.LpVariable.dicts("y2", Graph2.nodes(), cat=pulp.LpBinary)
    #print(y)
    x1 = pulp.LpVariable.dicts("x1", Graph1.edges(), cat=pulp.LpBinary)
    x2 = pulp.LpVariable.dicts("x2", Graph2.edges(), cat=pulp.LpBinary)
    # print(x)
    z = pulp.LpVariable("z", cat=pulp.LpContinuous)

    n = len(k)
    ## make optimisation problem
    prob = pulp.LpProblem("K-centreProblem", pulp.LpMinimize)

    ## add objective function
    prob += z

    ## add the first constraint set
    # Z is greater or equal to the weights of the edges in the solution
    for i in range(1,Graph1.number_of_nodes()+1):
        for j in range(1,Graph1.number_of_nodes()+1):
            prob += Graph1.edges[i,j]['weight'] * x1[i,j] <= z
            prob += Graph2.edges[i,j]['weight'] * x2[i,j] <= z



    ## add the second constraint set
    # every node is connected to at least one node in the solution
    for i in range(1,Graph1.number_of_nodes()+1):
        prob += pulp.lpSum( [x1[i,j] + x2[i,j] for j in Graph1.nodes()]) == 1

    ## add the third constraint set
    # nodes can only be connected to a node in the solution set
    for i in range(1,Graph1.number_of_nodes()+1):
        for j in range(1,Graph1.number_of_nodes()+1):
            if Graph1.has_edge(i,j) == True:
                prob += x1[i,j] <= y1[j]
                prob += x2[i,j] <= y2[j]


    ## add the fourth constraint set
    # the number of nodes in the solution set is equal to K
    prob += pulp.lpSum([y1[j] for j in Graph1.nodes()]) <= k[0]
    prob += pulp.lpSum([y2[j] for j in Graph2.nodes()]) <= k[1]

    ## solve the problem without any messages popping up
    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    # return the dominating set
    dominating_set = []
    for v in prob.variables():
        if v.varValue == 1.0:
            dominating_set.append(v.name)
    # return opt_dep and value of the objective function
    return dominating_set, pulp.value(prob.objective)


def visualize_Graph(G: nx.Graph):
    """
    Creates matplotlib figure with labeled and positioned nodes, and edges for a given graph G.
    """

    fig, ax = plt.subplots() # Initializes plot instance

    nx.draw_networkx(G, pos= nx.get_node_attributes(G, 'pos'), with_labels = True) # Draws graph with correct coordinates
    ax.tick_params(left = True, bottom = True, labelleft = True, labelbottom = True) # Adds axis units to aid understanding of graph
    
    # Make asset 1 red
    nx.draw_networkx_nodes(G, pos=nx.get_node_attributes(G, 'pos'), nodelist=[1,5], node_color='red', node_size=500)
    nx.draw_networkx_edges(G, pos=nx.get_node_attributes(G, 'pos'), edgelist=[(2,5), (3,5), (4,5), (5,5), (6,5), (7,5), (8, 5), (9, 5)], edge_color='red', width=3.0)
   

    # Make asset 2 blue
    nx.draw_networkx_nodes(G, pos=nx.get_node_attributes(G, 'pos'), nodelist=[11], node_color='blue', node_size=500)
    nx.draw_networkx_edges(G, pos=nx.get_node_attributes(G, 'pos'), edgelist=[(10, 11)], edge_color='blue', width=3.0)


    # Plot labels
    plt.xlabel("x")
    plt.ylabel("y")
    # plt.title("Graph")
    plt.show(block=True)


points = [
[47698.35491553461, 77923.64355529193],
[176627.18859639898, 142488.94821539056],
[196829.62248453422, 190801.6072196709],
[134785.5846269147, 182341.32591938227],
[144379.62522796058, 222638.98158654757],
[96976.09920786222, 188909.17587618623],
[76682.71996077016, 237778.4323344333],
[81365.48132678098, 266721.49994068407],
[163347.42061655904, 247797.18650582712],
[351813.6006496157, 336518.82066806685],
[344542.89127614786, 361454.38660575915]
]


speed1 = 41.7 # km/h
speed2 = 32.4 # km/h

# make an empty list with the dimensions of the points list
points1 = [[0,0] for i in range(len(points))]

# devide al coordinates by the speed to get the time in hours instead of km
for i in range(len(points)):
    points1[i][0] = points[i][0]/(1000 * speed1)
    points1[i][1] = points[i][1]/(1000 * speed1)
# print('points1:', points1)

# make an empty list with the dimensions of the points list
points2 = [[0,0] for i in range(len(points))]

# devide al coordinates by the speed to get the time in hours instead of km
for i in range(len(points)):
    points2[i][0] = points[i][0]/(1000 * speed2)
    points2[i][1] = points[i][1]/(1000 * speed2)
# print('points2:', points2)

"""	
#DSP test
max_times = [x/2 for x in range(2, 10)]

for time in max_times:
    Graph1 = create_Graph_DSP(points1, time)
    Graph2 = create_Graph_DSP(points2, time)
    for k in range(2,4):
        for l in range(0, 4):
            Feasible = DSP_LP(Graph1, Graph2, k, l)
            print("time:", time, "k:", k, "l:", l, "Feasible:", Feasible)



## solve KCP
for k1 in range(0,4):
    for k2 in range(0,4):
        Graph1 = create_graph_KCP(points1)
        Graph2 = create_graph_KCP(points2)
        dominating_set, opt_dep = KCP_Multi_LP(Graph1, Graph2, [k1,k2])
        print("k1:", k1, "k2:", k2, "dominating set:", dominating_set, "optimal interdiction time:", opt_dep)
"""	



Graph = create_Graph_DSP(points1, 999)
visualize_Graph(Graph)

