import networkx as nx
import math

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