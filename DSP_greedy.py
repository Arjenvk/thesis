### Python script to solve the DSP with a greedy heuristic
### Input: G, max lengths
### Output: A minimum dominating set of G

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
    plt.show(block=False)

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

    return removed_nodes



points = [[1, 8], [6, 3], [5,6], [5, 8], [9, 1], [4,9], [8,9], [3,1]]
max_length = 6

Graph = create_Graph(points, max_length)
visualize_Graph(Graph)

min_dom_set = DSP_GREEDY(Graph)
print("Minimum dominating set: ", min_dom_set)
