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
print('points1:', points1)


RF1_tot = []
RF2_tot = []
set__old_reaction_time = []
set_worst_case_reaction_time = []
set_average_reaction_time = []
# iterate over K from 2 to 11
for K in range(2,11):
    print("K is:", K)
    # make graph
    Graph = create_graph_KCP(points1)
    # solve initial k centre problem
    opt_dep, reaction_time = KCP_LP(Graph, K)
    set__old_reaction_time.append(reaction_time)
    print("The initial optimal deployment is:", opt_dep, "for K : ", K ," with a reaction time of:", reaction_time, 'hours')

    set_reaction_time = []
    # remove the points one by one from the points1 list and solve the k centre problem again
    for i in range(len(points1)):
        # make a working points copy
        points2 = points1.copy()
        # remove the point from the points1 list
        points2.pop(i)
        # solve the new k centre problem
        Graph = create_graph_KCP(points2)
        new_opt_dep, new_reaction_time = KCP_LP(Graph, K-1)
        # print("The new optimal deployment is:", new_opt_dep, "for K : ", K ," with a reaction time of:", new_reaction_time, 'hours')
        set_reaction_time.append(new_reaction_time)

    # calculate average of the reaction times
    average_reaction_time = sum(set_reaction_time)/len(set_reaction_time)
    set_average_reaction_time.append(average_reaction_time)
    print('set_reaction_time:', set_reaction_time)
    print('The original interdiction time is:', reaction_time, 'hours')
    print('The worst case interdiction time is:', max(set_reaction_time), 'hours')
    set_worst_case_reaction_time.append(max(set_reaction_time))
    print('The average interdiction time is:', average_reaction_time, 'hours')
    RF1 = reaction_time / max(set_reaction_time)
    RF1_tot.append(RF1)
    RF2 = reaction_time / average_reaction_time
    RF2_tot.append(RF2)
    print('The robustness factor RF1 is:', RF1)
    print('The robustness factor RF2 is:', RF2)

# plot the reaction times
K = range(2,11)
plt.plot(K, set__old_reaction_time, label = 'Original max interdiction time')
plt.plot(K, set_worst_case_reaction_time, label = 'Worst case max interdiction time')
plt.plot(K, set_average_reaction_time, label = 'Average max interdiction time')
plt.xlabel('K')
plt.ylabel('Max interdiction time [hours]')
plt.legend()
plt.show()



# Plot the RF1 and RF2
K = range(2,11)
plt.plot(K, RF1_tot, label = 'RF1')
plt.plot(K, RF2_tot, label = 'RF2')
plt.xlabel('K')
plt.ylabel('Robustness Factor')
plt.legend()
plt.show()
