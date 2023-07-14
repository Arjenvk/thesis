### Python function to solve the DSP with linear programming
### Input: G, max lengths
### Output: A minimum dominating set of G

import pulp
import networkx as nx
import math
import matplotlib.pyplot as plt
import time

def create_Graph(points, max_length):
    G = nx.Graph()
    # add nodes
    k = 1
    G.add_node(k, pos=(points[k-1]))
   #  print("node", k, "added. coordinates: ", points[k-1])
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
def DSP_LP(Graph):
    min_sets = []
    y = pulp.LpVariable.dicts("y", Graph.nodes(), cat=pulp.LpBinary)
    prob = pulp.LpProblem("MinimumDominatingSet", pulp.LpMinimize)
    prob += pulp.lpSum(y)
    for i in Graph.nodes():
        prob += y[i] + pulp.lpSum([y[j] for j in Graph.neighbors(i)]) >= 1

    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    return pulp.value(prob.objective)
def visualize_Graph(G: nx.Graph):
    """
    Creates matplotlib figure with labeled and positioned nodes, and edges for a given graph G.
    """

    fig, ax = plt.subplots() # Initializes plot instance

    nx.draw_networkx(G, pos= nx.get_node_attributes(G, 'pos'), with_labels = True) # Draws graph with correct coordinates
    ax.tick_params(left = True, bottom = True, labelleft = True, labelbottom = True) # Adds axis units to aid understanding of graph
    
    # Make asset 1 red
    #nx.draw_networkx_nodes(G, pos=nx.get_node_attributes(G, 'pos'), nodelist=[1,5], node_color='red', node_size=500)
    #nx.draw_networkx_edges(G, pos=nx.get_node_attributes(G, 'pos'), edgelist=[(2,5), (3,5), (4,5), (5,5), (6,5), (7,5), (8, 5), (9, 5)], edge_color='red', width=3.0)
   
    # Make asset 2 blue
    #nx.draw_networkx_nodes(G, pos=nx.get_node_attributes(G, 'pos'), nodelist=[11], node_color='blue', node_size=500)
    #nx.draw_networkx_edges(G, pos=nx.get_node_attributes(G, 'pos'), edgelist=[(10, 11)], edge_color='blue', width=3.0)


    # Plot labels
    plt.xlabel("x")
    plt.ylabel("y")
    # plt.title("Graph")
    plt.show(block=True)

points_dk = [
(64172.79213556182, 124797.84441804112),
(52179.67547545768, 182264.59093855572),
(52213.29396167677, 182319.69240863965),
(52280.308295134455, 182454.93149142695),
(52179.564155966975, 182377.69988462474),
(53508.83019552939, 180436.20746056963),
(53407.64077839814, 179558.97105676745),
(53310.458862936124, 179436.92551360425),
(53234.09369225148, 179264.6985943757),
(53353.650825363584, 179298.8980664906),
(53470.313651714474, 179647.71126175398),
(53129.78732937761, 179451.34297078563),
(64465.67371583916, 140391.10779694765),
(64401.776328123175, 140365.304082878),
(64525.340962904505, 140484.82785292395),
(64458.549268427305, 140636.18766014726),
(64648.68295870349, 140614.6286435732),
(64386.97083584778, 140301.07409627753),
(44755.444675982, 176203.24126472528),
(67458.05294785276, 110641.49427734088),
(59080.92730718665, 157203.80824895768),
(59112.319403590634, 157277.99648796505),
(59170.87345574796, 157028.84049573593),
(131175.88232454285, 75792.57633220428),
(92874.74172475468, 118456.11803573678),
(59012.131861876696, 168087.48092567903),
(165051.8505263161, 157515.9803434477),
(182653.57709105778, 203337.39690131234),
(156082.72783361096, 140588.26633100578),
(186434.6549153421, 213546.2874618583),
(120041.70685539953, 81322.78114035417),
(59888.99549085554, 170895.9277868283),
(59110.42697224673, 167927.90824660385),
(59133.58142633177, 168143.8007779299),
(53030.37902410049, 179591.829507761),
(92814.29524125438, 118510.05621186749),
(89506.99316978548, 118770.70207119483),
(59924.50640841853, 170977.39358226204),
(59965.47198103089, 171163.6812791188),
(59779.45711191464, 170767.52715046034),
(165974.13250753842, 160646.71210657124),
(121612.64750947338, 84368.03259758255),
(121977.21884182189, 80249.19402178883),
(120027.7919190498, 81546.80957662594),
(138790.91473123804, 51188.59928350325),
(98168.98538739234, 56113.121654213464)]
# switch positions of coordinates
for i in range(len(points_dk)):
    points_dk[i] = [points_dk[i][1], points_dk[i][0]]

# state how many oil rigs Denmark operates
print("Denmark operates", len(points_dk), "oil rigs")
# visualize graph
Graph = create_Graph(points_dk, 9999999999)
# visualize_Graph(Graph)

speed= 150
# make an empty list with the dimensions of the points list
points1 = [[0,0] for i in range(len(points_dk))]

 # devide al coordinates by the speed to get the time in hours instead of km
for i in range(len(points_dk)):
    points1[i][0] = points_dk[i][0]/(1000 * speed)
    points1[i][1] = points_dk[i][1]/(1000 * speed)

# make a list of maximum times from 0 to 5 hours in steps of 0.1 hours
max_times = [x/10 for x in range(0, 51)]

min_set_size = []
# determine the minimum dominating set for each maximum time
for max_time in max_times:
    Graph = create_Graph(points1, max_time)
    min_set_size.append(DSP_LP(Graph))
    # print("The minimum dominating set cardinality for a speed of", speed, " kmh and a maximum time of", max_time, "hours is:", min_set_size[-1])

# plot the minimum dominating set size as a function of the maximum time
plt.plot(max_times, min_set_size)
plt.xlabel("Maximum time (hours)")
plt.ylabel("Minimum dominating set size")
# set y axis limit
plt.ylim(0, 10)
plt.xlim(0, 3)
# plt.title("Minimum dominating set size as a function of the maximum time")
plt.show()

print(min_set_size)
