import networkx as nx
import random
import math
import matplotlib.pyplot as plt
from create_graph import create_graph_KCP
import time


def calculate_cost(G, centers):
    max_distance = 0
    for node in G:
        min_distance_to_center = min([nx.dijkstra_path_length(G, node, center) for center in centers])
        max_distance = max(max_distance, min_distance_to_center)
    return max_distance

def KCP_SA(G, k, T, alpha, stopping_T, stopping_iter):
    current_centers = random.sample(list(G.nodes()), k)
    current_cost = calculate_cost(G, current_centers)
    
    for i in range(stopping_iter):
        if T <= stopping_T:
            break
        candidate_centers = current_centers[:]
        candidate_centers[random.randint(0, k-1)] = random.choice(list(G.nodes()))
        candidate_cost = calculate_cost(G, candidate_centers)
        
        cost_diff = current_cost - candidate_cost
        
        if cost_diff > 0 or random.uniform(0, 1) < math.exp(cost_diff / T):
            current_centers = candidate_centers
            current_cost = candidate_cost
        
        T *= alpha
    
    return current_centers, current_cost


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

# Set initial parameters
T = 1.0
alpha = 0.95
stopping_T = 0.001
stopping_iter = 100


opt_deps_1 = []
reaction_times_1 = []
clocks = []
random.seed(0)
for K in range(1, len(points)+1):
    start = time.time()
    print("K is:", K)
    opt_dep, reaction_time = KCP_SA(Graph, K, T, alpha, stopping_T, stopping_iter)
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

# Set initial parameters
T = 1.0
alpha = 0.95
stopping_T = 0.001
stopping_iter = 100


opt_deps_2 = []
reaction_times_2 = []
clocks = []
random.seed(0)
for K in range(1, len(points)+1):
    start = time.time()
    print("K is:", K)
    opt_dep, reaction_time = KCP_SA(Graph, K, T, alpha, stopping_T, stopping_iter)
    opt_deps_2.append(opt_dep)
    reaction_times_2.append(round(reaction_time,2))
    stop = time.time()
    # print("The optimal deployment is:", opt_dep, "with a reaction time of:", reaction_time, 'hours')
    clocks.append(round(stop-start,2))

print('clocks:', clocks)
print('opt_deps_2:', opt_deps_2)
print('reaction_times_2:', reaction_times_2)    
