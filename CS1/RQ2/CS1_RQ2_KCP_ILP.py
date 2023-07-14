### Python function to solve the KCP with linear programming
### Based on the LP formulation of M. S. Daskin in: Network and discrete location: Models, Algorithms, and Applications. New York: Wiley, 1995.
### Input: Graph, k, max lengths
### Output: A minimum K centre location(s) of G

import pulp
import networkx as nx
import math
import time
import matplotlib.pyplot as plt
from create_graph import create_graph_KCP


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
    for l in range(1,Graph.number_of_nodes()+1):
        for k in range(1,Graph.number_of_nodes()+1):
            # print('l is:', l, 'k is:', k)
            # print(' constraint of edge', l, 'to', k, 'is added with a length of:', Graph.edges[l,k]['weight'])
            prob += Graph.edges[l,k]['weight'] * x[l,k] <= z


    ## add the second constraint set
    # every node is connected to at least one node in the solution
    for l in range(1,Graph.number_of_nodes()+1):
        prob += pulp.lpSum([x[l,k] for k in Graph.nodes()]) == 1

    ## add the third constraint set
    # nodes can only be connected to a node in the solution set
    for l in range(1,Graph.number_of_nodes()+1):
        for k in range(1,Graph.number_of_nodes()+1):
            if Graph.has_edge(l,k) == True:
                prob += x[l,k] <= y[k]


    ## add the fourth constraint set
    # the number of nodes in the solution set is equal to K
    prob += pulp.lpSum([y[l] for l in Graph.nodes()]) <= K

    ## solve the problem without any messages popping up
    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    # return the dominating set
    dominating_set = []
    for v in prob.variables():
        if v.varValue == 1.0:
            dominating_set.append(v.name)
    # return opt_dep and value of the objective function
    return dominating_set, pulp.value(prob.objective)



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

## asset type 1

# make an empty list with the dimensions of the points list
points1 = [[0,0] for i in range(len(points))]

# devide al coordinates by the speed to get the time in hours instead of km
for i in range(len(points)):
    points1[i][0] = points[i][0]/(1000 * speed1)
    points1[i][1] = points[i][1]/(1000 * speed1)

# make graph
Graph = create_graph_KCP(points1)


opt_deps_1 = []
reaction_times_1 = []
clocks = []
for K in range(1, len(points)+1):
    start = time.time()
    print("K is:", K)
    opt_dep, reaction_time = KCP_LP(Graph, K)
    opt_deps_1.append(opt_dep)
    reaction_times_1.append(reaction_time)
    stop = time.time()
    # print("The optimal deployment is:", opt_dep, "with a reaction time of:", reaction_time, 'hours')
    clocks.append(round(stop-start,2))

print('clocks:', clocks)
print('opt_deps_1:', opt_deps_1)
print('reaction_times_1:', reaction_times_1)    

## asset type 2

# make an empty list with the dimensions of the points list
points2 = [[0,0] for i in range(len(points))]

# devide al coordinates by the speed to get the time in hours instead of km
for i in range(len(points)):
    points2[i][0] = points[i][0]/(1000 * speed2)
    points2[i][1] = points[i][1]/(1000 * speed2)

# make graph
Graph = create_graph_KCP(points2)


opt_deps_2 = []
reaction_times_2 = []
clocks = []
for K in range(1, len(points)+1):
    start = time.time()
    print("K is:", K)
    opt_dep, reaction_time = KCP_LP(Graph, K)
    opt_deps_2.append(opt_dep)
    reaction_times_2.append(reaction_time)
    print("The optimal deployment is:", opt_dep, "with a reaction time of:", reaction_time, 'hours')
    stop = time.time()
    clocks.append(round(stop-start,2))



# plot the reaction times
plt.plot(range(1, len(points)+1), reaction_times_1, label='asset type 1')
plt.plot(range(1, len(points)+1), reaction_times_2, label='asset type 2')
plt.xlabel('K')
plt.ylabel('reaction time (hours)')
plt.legend()
plt.show()

print('clocks:', clocks)
print('opt_deps_2:', opt_deps_2)
print('reaction_times_2:', reaction_times_2)

