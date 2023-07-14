### Python script to solve the DSP with brute force
### Input: G, max lengths
### Output: all minimum dominating sets of G

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

def visualize_Graph(G: nx.Graph):
    """
    Creates matplotlib figure with labeled and positioned nodes, and edges for a given graph G.
    """

    fig, ax = plt.subplots() # Initializes plot instance

    nx.draw_networkx(G, pos= nx.get_node_attributes(G, 'pos'), with_labels = True) # Draws graph with correct coordinates
    ax.tick_params(left = True, bottom = True, labelleft = True, labelbottom = True) # Adds axis units to aid understanding of graph

    # Plot labels
    plt.xlabel("x [hours]")
    plt.ylabel("y [hours]" )
    # plt.title("Graph")
    plt.show()
    
def is_dom_set(G, D):
    """
    Returns a boolean whether the subset of G is a dominant set or not.
    """

    edges = G.edges
    V = G.nodes

    is_dom = False
    for d in D:
        for v in V:
            if v not in D: #and len(D) != 1: # verifies if node is in subset D, if not, verifies if its adjacent to any another node in the set
                for d2 in D:
                    if (d2,v) in edges or (v,d2) in edges: # checks if nodes are adjacent
                        is_dom = True
                        break
                    else:
                        is_dom = False
                if is_dom == True:
                    continue
                else: 
                    return False
                    
    return True

def find_dom_sets(G):
    """
    Finds all possible dominating sets in a given graph G. 
    """

    nodes_arr = G.nodes
    subsets = [list(S) for l in range(0, len(nodes_arr)) for S in itertools.combinations(nodes_arr, l+1)] # every possible set of vertices from G
    dom_sets = []

    for D in subsets: 
        if len(D) == len(G):
            dom_sets.append(tuple(D))
            continue

        if is_dom_set(G, D):
            dom_sets.append(tuple(D)) #list with every dominant set of given graph

    return dom_sets

def find_minimum_dom_sets(G):
    """
    Finds all the minimum dominant sets in a given graph G.
    """
    dom_sets = find_dom_sets(G)
    min_len = min([len(x) for x in dom_sets])
    min_sets = [x for x in dom_sets if len(x) == min_len]

    return min_sets


## case study 1

start = time.time()


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


## asset type 1

# make an empty list with the dimensions of the points list
points1 = [[0,0] for i in range(len(points))]

# devide al coordinates by the speed to get the time in hours instead of km
for i in range(len(points)):
    points1[i][0] = points[i][0]/(1000 * speed1)
    points1[i][1] = points[i][1]/(1000 * speed1)

# emmpty list of minimum dominating sets lengths
min_set_lengths_type1 = []

# determine the minimum dominating set for each maximum time
for max_time in max_times:
    Graph = create_Graph(points1, max_time)
    dom_sets = find_dom_sets(Graph)
    min_sets = find_minimum_dom_sets(Graph)
    print("The minimum dominating sets for a maximum time of", max_time, "hours are:",min_sets, "with a size of", len(min_sets[0]))
    # add the length of the minimum dominating set to the list
    min_set_lengths_type1.append(len(min_sets[0]))


## asset type 2

# make an empty list with the dimensions of the points list
points2 = [[0,0] for i in range(len(points))]


# devide al coordinates by the speed to get the time in hours instead of km
for i in range(len(points)):
    points2[i][0] = points[i][0]/(1000 * speed2)
    points2[i][1] = points[i][1]/(1000 * speed2)


# emmpty list of minimum dominating sets lengths
min_set_lengths_type2 = []

# determine the minimum dominating set for each maximum time
for max_time in max_times:
    Graph = create_Graph(points2, max_time)
    dom_sets = find_dom_sets(Graph)
    min_sets = find_minimum_dom_sets(Graph)
    print("The minimum dominating sets for a maximum time of", max_time, "hours are:",min_sets, "with a size of", len(min_sets[0]))
    # add the length of the minimum dominating set to the list
    min_set_lengths_type2.append(len(min_sets[0]))


end = time.time()
print('Elapsed time is:', round(end - start, 2), 'seconds')


# make a graph of the minimum dominating set lengths
plt.plot(max_times, min_set_lengths_type1)
plt.plot(max_times, min_set_lengths_type2)
plt.legend(["Asset type 1", "Asset type 2"])
plt.xlabel("Maximum reaction time [hours]")
plt.ylabel("Minimum dominating set cardinality")
plt.show()
