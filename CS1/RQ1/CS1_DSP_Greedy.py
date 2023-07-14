### Python script to solve the DSP with a greedy heuristic
### Input: G, max lengths
### Output: A minimum dominating set of G

import matplotlib.pyplot as plt
import networkx as nx
import math
import itertools
import time

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
    for k in range(1,len(points)+1):
        for l in range(1,len(points)+1):
            if k != l:
                length = math.sqrt((points[k-1][0] - points[l-1][0])**2 + (points[k-1][1] - points[l-1][1])**2)
                if length < max_length:
                    # check if reverse arc is already in set
                    if (l,k) not in seen_edge and (k,l) not in seen_edge:
                        G.add_edge(k, l)
                        seen_edge.add((k,l))
                        print("edge", k, "to", l, "added")
    return G


def DSP_GREEDY(G):
    """
    Greedy heuristic based algorithm to find a minimum dominating set of graph G.
    """

    edges = [list(e) for e in G.edges]
    edge_count = {node : 0 for node in G.nodes} # node dictionary with edge counts -> {node: n_of_edges}

    removed_nodes = []

    while len(edge_count) > 0: # Iterates over nodes until there are none left

        # Counts the number of edges of each node
        for edge in edges:
            for node in list(edge_count.keys()):
                if node == edge[0] or node == edge[1]:
                    edge_count[node] += 1

        max_idx = list(edge_count.values()).index(max(edge_count.values())) # index of node with most edges
        node_to_rem = list(edge_count.keys())[max_idx] # Main node which will be removed
        removed_nodes.append(node_to_rem) # list of removed nodes which will be the minimum dominating set later
        
        adjacent_nodes= []

        for edge in reversed(edges):
            # Adds the adjacent node to a list and removes the main node edge
            if edge[0] == node_to_rem:
                adjacent_nodes.append(edge[1])
                edges.remove(edge)
            elif edge[1] == node_to_rem:
                adjacent_nodes.append(edge[0])
                edges.remove(edge) 

        # Removed adjacent nodes' edges
        for adj_node in adjacent_nodes:
            for edge in reversed(edges):
                if edge[0] == adj_node or edge[1] == adj_node:
                    edges.remove(edge)
        
        del edge_count[node_to_rem] # Remove main node from dictionary

        # Remove adjacent nodes from dictionary
        for adj_node in adjacent_nodes:
            del edge_count[adj_node]

        # Reset edge count with remaining nodes
        edge_count = {n:0 for n in edge_count}

    # return number of nodes in minimum dominating set
    return len(removed_nodes)


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

# make a list of maximum times from 0 to 5 hours in steps of 0.1 hours
max_times = [x/10 for x in range(0, 51)]

start = time.time()
## asset type 1

# make an empty list with the dimensions of the points list
points1 = [[0,0] for i in range(len(points))]

# devide al coordinates by the speed to get the time in hours instead of km
for i in range(len(points)):
    points1[i][0] = points[i][0]/(1000 * speed1)
    points1[i][1] = points[i][1]/(1000 * speed1)

min_set_sizes_type1 = []
# determine the minimum dominating set for each maximum time
for max_time in max_times:
    Graph = create_Graph(points1, max_time)
    min_set_sizes_type1.append(DSP_GREEDY(Graph))
    print("The minimum dominating set cardinality for a maximum time of", max_time, "hours is:", min_set_sizes_type1[-1])

## asset type 2

# make an empty list with the dimensions of the points list
points2 = [[0,0] for i in range(len(points))]

# devide al coordinates by the speed to get the time in hours instead of km
for i in range(len(points)):
    points2[i][0] = points[i][0]/(1000 * speed2)
    points2[i][1] = points[i][1]/(1000 * speed2)

min_set_sizes_type2 = []
# determine the minimum dominating set for each maximum time
for max_time in max_times:
    Graph = create_Graph(points2, max_time)
    min_set_sizes_type2.append(DSP_GREEDY(Graph))
    print("The minimum dominating set cardinality for a maximum time of", max_time, "hours is:", min_set_sizes_type1[-1])


stop = time.time()
print("The total time is:", stop - start)


# make a graph of the minimum dominating set lengths
plt.plot(max_times, min_set_sizes_type1)
plt.plot(max_times, min_set_sizes_type2)
plt.legend(["Asset type 1", "Asset type 2"])
plt.xlabel("Maximum reaction time [hours]")
plt.ylabel("Minimum dominating set cardinality")
plt.show()
