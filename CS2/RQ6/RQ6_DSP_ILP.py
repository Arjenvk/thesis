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
def create_Graph_KCP(points, VF):
    G = nx.DiGraph()
    # add nodes
    k = 1
    G.add_node(k, pos=(points[k-1]), vulnerability=VF[k-1])
    # print("node", k, "added. coordinates: ", points[k-1], "vulnerability factor:", VF[k-1])
    while len(list(G)) < len(points):
        k += 1
        G.add_node(k, pos=(points[k-1]), vulnerability=VF[k-1])
        # print("node", k, "added. coordinates: ", points[k-1], "vulnerability factor:", VF[k-1])

    # add edges to make a complete graph
    for k in range(1, len(points)+1):
        for l in range(1, len(points)+1):
            if k == l:
                G.add_edge(k, l, weight=0)
            elif k != l:
                length = math.sqrt((points[k-1][0] - points[l-1][0])**2 + (points[k-1][1] - points[l-1][1])**2)
                G.add_edge(k, l, weight=length)
                # print("edge", k, "to", l, "added with weight", length)
    return G  
def KCP_LP_weighted(Graph, K):
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
    for i in range(1,Graph.number_of_nodes()+1):
        for j in range(1,Graph.number_of_nodes()+1):
            # print('l is:', l, 'k is:', k)
            prob += Graph.edges[i,j]['weight'] * Graph.nodes[i]['vulnerability'] * x[i,j] <= z
            # print(' constraint of edge', l, 'to', k, 'is added with a length of:', Graph.edges[l,k]['weight'], 'and a vulnerability factor of:', Graph.nodes[k]['vulnerability'])


    ## add the second constraint set
    # every node is connected to at least one node in the solution
    for i in range(1,Graph.number_of_nodes()+1):
        prob += pulp.lpSum([x[i,j] for j in Graph.nodes()]) == 1

    ## add the third constraint set
    # nodes can only be connected to a node in the solution set
    for i in range(1,Graph.number_of_nodes()+1):
        for j in range(1,Graph.number_of_nodes()+1):
            prob += x[i,j] <= y[j]


    ## add the fourth constraint set
    # the number of nodes in the solution set is equal to K
    prob += pulp.lpSum([y[j] for j in Graph.nodes()]) <= K

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
[373142.93313905224, 245178.90046394226],
[314366.2420002045, 22063.96603759093],
[271730.87702638004, 124411.68360544613],
[291545.7463875832, 167922.58408434788],
[284198.6599952262, 327767.3946252318],
[258817.81609436125, 49370.3412317232],
[244457.60178202763, 93519.27205719339],
[245014.1992359953, 152189.4322566245],
[227425.71969065722, 189015.97320441325],
[240561.41960426327, 226751.42042757146],
[235440.72302777413, 274672.00509915495],
[228761.55358017702, 384821.83712024783],
[222750.3010773398, 96530.05082767695],
[218186.20195481554, 156317.7327908998],
[211840.99097959884, 190243.78570825414],
[213065.50537832547, 222843.10706529638],
[212174.94945197925, 254673.53713449446],
[191469.52416442987, 80027.52985115355],
[196812.8597225072, 125638.6481360973],
[194586.4699066421, 165467.5899646241],
[159966.1082699336, 74118.43182016228],
[167424.51415308286, 153193.5968248422],
[167869.79211625643, 167922.58408434788],
[163973.60993849114, 206541.8659319412],
[139594.64145476464, 140028.722308203],
[158296.31590803433, 178078.0378384657],
[142600.26770618279, 190243.78570825414],
[100410.18069553282, 140028.722308203],
[110874.21283010021, 219716.5916682883],
[87719.75874509849, 148172.8802973128],
[38071.26585129928, 64642.20541318745]]
# switch positions of coordinates
for i in range(len(points)):
    points[i] = [points[i][1], points[i][0]]

weights = [24,36,36,24,18,24,24,12,10,6,24,36,24,14,14,36,36,36,36,36,40,36,36,24,14,20,8,8,20,10,40]
VF = []
for i in range(1,len(points)+1):
    VF.append(1 + (weights[i-1] - 6)/(40-6))

eai = []
for k in range(1,len(points)+1):
    eai.append(VF[k-1]/sum(VF))
print('eai is:', eai)

"""	
# visualize graph
Graph = create_Graph(points, 9999999999)
visualize_Graph(Graph)

speeds = range(10, 75, 10)

for speed in speeds:
    # make an empty list with the dimensions of the points list
    points1 = [[0,0] for i in range(len(points))]

    # devide al coordinates by the speed to get the time in hours instead of km
    for i in range(len(points)):
        points1[i][0] = points[i][0]/(1000 * speed)
        points1[i][1] = points[i][1]/(1000 * speed)
    # make a list of maximum times from 0 to 5 hours in steps of 0.1 hours
    max_times = [x/10 for x in range(0, 51)]

    min_set_size = []
    # determine the minimum dominating set for each maximum time
    for max_time in max_times:
        Graph = create_Graph(points1, max_time)
        min_set_size.append(DSP_LP(Graph))
        # print("The minimum dominating set cardinality for a speed of", speed, " kmh and a maximum time of", max_time, "hours is:", min_set_size[-1])

    # plot the minimum dominating set cardinality against the maximum time for this speed
    plt.plot(max_times, min_set_size, label = "speed =" + str(speed) + "kmh")

plt.xlabel("Maximum interdiction time (hours)")
plt.ylabel("Minimum dominating set cardinality")
plt.legend()
plt.show()
"""

speeds = range(30, 75, 10)

for speed in speeds:
    print('---------------------------------------------')
    print('speed:', speed)
    print('---------------------------------------------')
    # make an empty list with the dimensions of the points list
    points1 = [[0,0] for i in range(len(points))]
    # devide al coordinates by the speed to get the time in hours instead of km
    for i in range(len(points)):
        points1[i][0] = points[i][0]/(1000 * speed)
        points1[i][1] = points[i][1]/(1000 * speed)
    
    RF1_tot = []
    RF2_tot = []
    set_old_reaction_time = []
    set_worst_case_reaction_time = []
    set_est_inter_time = []
    for k in range(1,6):
        print('---------------------------------------------')
        print('k:', k)
        print('---------------------------------------------')
        Graph = create_Graph_KCP(points1, VF)
        opt_dep, inter_time = KCP_LP_weighted(Graph, k)
        set_old_reaction_time.append(inter_time)
        print("The initial optimal deployment is:", opt_dep, "for K : ", k ," with a reaction time of:", inter_time, 'hours')
        """
        set_reaction_time = []
        # remove the points one by one from the points1 list and solve the k centre problem again
        for i in range(len(points1)):
            # make a working points copy
            points2 = points1.copy()
            VF2 = VF.copy()
            # remove the point from the points1 list
            points2.pop(i)
            VF2.pop(i)
            # solve the new k centre problem
            Graph = create_Graph_KCP(points2, VF2)
            new_opt_dep, new_inter_time = KCP_LP_weighted(Graph, k-1)
            # print("The new optimal deployment is:", new_opt_dep, "for K : ", K ," with a reaction time of:", new_reaction_time, 'hours')
            set_reaction_time.append(new_inter_time)

        # calculate average of the reaction times
        # sum the product of two lists
        est_inter_time = sum([a*b for a,b in zip(eai, set_reaction_time)])
        set_est_inter_time.append(est_inter_time)
        print('set_reaction_time:', set_reaction_time)
        print('The original interdiction time is:', inter_time, 'hours')
        print('The worst case interdiction time is:', max(set_reaction_time), 'hours')
        # show index of the worst case reaction time
        print('The worst case reaction time is at index:', set_reaction_time.index(max(set_reaction_time)))
        set_worst_case_reaction_time.append(max(set_reaction_time))
        print('The estimated interdiction time is:', est_inter_time, 'hours')
        RF1 = inter_time / max(set_reaction_time)
        RF1_tot.append(RF1)
        RF2 = inter_time / est_inter_time
        RF2_tot.append(RF2)
        print('The robustness factor RF1 is:', RF1)
        print('The robustness factor RF2 is:', RF2)
        """

    # plot the maximum interdction time against k for this speed
    plt.plot(range(1,6), set_old_reaction_time, label = "speed = " + str(speed) + "kmh")

plt.xlabel("K")
# set x axis on integers
plt.xticks(range(1,6))
plt.ylabel("Interdiction time (hours)")
plt.legend()
plt.show()