### Python script to solve the DSP with brute force
### Input: G, max lengths
### Output: all minimum dominating sets of G

import matplotlib.pyplot as plt
import networkx as nx
import math
import itertools


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
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Graph")
    plt.show(block=True)
    
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

points = [[1, 8], [6, 3], [5,6], [5, 8], [9, 1], [4,9], [8,9], [3,1], [2,3]]
max_length = 5

Graph = create_Graph(points, max_length)
visualize_Graph(Graph)

dom_sets = find_dom_sets(Graph)
min_sets = find_minimum_dom_sets(Graph)
print("The minimum dominating sets are:",min_sets, "with a size of", len(min_sets[0]))