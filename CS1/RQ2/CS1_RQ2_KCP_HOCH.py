import networkx as nx
from heapq import heappop, heappush
import time
import matplotlib.pyplot as plt
import math
from create_graph import create_graph_KCP

def hochbaum_k_center(Graph, k):
    # Function to calculate the shortest path lengths from a node to all other nodes
    def shortest_path_lengths(Graph, node):
        visited = {node: 0}
        heap = [(0, node)]
        while heap:
            (dist, v) = heappop(heap)
            for u in Graph.neighbors(v):
                if u not in visited or visited[u] > dist + Graph.edges[v, u]['weight']:
                    visited[u] = dist + Graph.edges[v, u]['weight']
                    heappush(heap, (visited[u], u))
        return visited

    # Start with one node arbitrarily
    node = list(Graph.nodes())[0]
    centers = [node]
    sp_lengths = shortest_path_lengths(Graph, node)

    # Add k-1 centers
    for _ in range(k - 1):
        node = max(sp_lengths, key=sp_lengths.get)
        centers.append(node)
        new_sp_lengths = shortest_path_lengths(Graph, node)
        for v in sp_lengths:
            sp_lengths[v] = min(sp_lengths[v], new_sp_lengths[v])

    # return centres and the maximum distance from a center to a node
    return centers, max(sp_lengths.values())


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
    opt_dep, reaction_time = hochbaum_k_center(Graph, K)
    opt_deps_1.append(opt_dep)
    reaction_times_1.append(round(reaction_time,2))
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
clocks2 = []
for K in range(1, len(points)+1):
    start = time.time()
    print("K is:", K)
    opt_dep, reaction_time = hochbaum_k_center(Graph, K)
    opt_deps_2.append(opt_dep)
    reaction_times_2.append(round(reaction_time,2))
    stop = time.time()
    # print("The optimal deployment is:", opt_dep, "with a reaction time of:", reaction_time, 'hours')
    clocks2.append(round(stop-start,2))

print('clocks:', clocks2)
print('opt_deps_2:', opt_deps_2)
print('reaction_times_2:', reaction_times_2)    


# plot the reaction times
plt.plot(range(1, len(points)+1), reaction_times_1, label='asset type 1')
plt.plot(range(1, len(points)+1), reaction_times_2, label='asset type 2')
plt.xlabel('K')
plt.ylabel('reaction time (hours)')
plt.legend()
plt.show()

