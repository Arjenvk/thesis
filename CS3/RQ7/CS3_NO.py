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

points_no = [
 (169244.47650806326, 191796.26866713804),
(182794.61888589244, 203565.25365845484),
(172046.05413285736, 191113.9172037438),
(130896.02512468863, 218248.98736972138),
(142142.07668207958, 211175.56603536432),
(162990.65883478802, 178596.49674963832),
(172160.82452786528, 190711.86693543583),
(172135.10972549208, 191034.86727449202),
(495421.8278009249, 96378.71532305013),
(508390.1032003788, 55330.458080325916),
(466542.88022137154, 98665.40171577773),
(616937.1820754455, 172143.59360751158),
(172420.1989414133, 190650.2104336526),
(526943.1661334392, 117644.66129790622),
(174180.38272983674, 189658.69373061534),
(172287.84006686043, 190866.06408337774),
(172230.95580706466, 190977.55889751107),
(172159.60001346655, 191620.55162391832),
(174230.4765006937, 189928.17402804174),
(171956.66458175052, 191816.89536834924),
(171956.66458175052, 191816.89536834924),
(172208.3579504341, 191359.76394992127),
(153199.10774410143, 196585.443757306),
(157924.62012827676, 191299.11055361023),
(157803.17056382075, 191416.51504306463),
(152999.28925812803, 196518.76653311608),
(153069.8658152921, 196599.93881129494),
(148339.78933199495, 194629.96663943524),
(385248.3711653687, 45312.6811441179),
(704862.7705590222, 266941.853118574),
(463607.8305271147, 109804.7452424329),
(687464.6473429408, 76562.89500365578),
(690449.3455300899, 77916.30718381162),
(691788.5190043328, 86001.0293811957),
(211982.4780523982, 176446.23330016402),
(413295.6508292062, 18545.455448941502),
(495893.37716392614, 98545.74090399445),
(611293.2838922264, 147678.2971080705),
(611457.4801411452, 147782.95339591426),
(624259.6668603355, 141913.4148564024),
(611160.034461746, 147864.6500032119),
(599972.5369565133, 144295.90480601418),
(634519.3164098077, 159704.41185161695),
(474831.39554736577, 105622.26898530973),
(342558.1256825831, 43310.726416687656),
(717881.6963267857, 71569.43425628927),
(726353.8888125895, 79050.93605971299),
(696323.0071423063, 39215.32642725238),
(690893.3989788648, 36627.37160387015),
(700876.1969547328, 44636.26449109882),
(220646.69665982015, 162353.30760829386),
(342562.244503743, 43311.951596825354),
(642744.602265032, 223031.07423565324),
(655207.1532178102, 235105.7674009721),
(306534.35922544356, 318218.440127678),
(313418.80181406345, 338247.3847414695),
(234971.06609611772, 149929.7077542272),
(235007.24493062496, 150067.80298571996),
(234932.10427433904, 149779.57533441295),
(142209.75893248152, 211029.59270647258),
(147352.60808763932, 206268.895970881),
(136593.24534399714, 215720.91133739127),
(142026.41573114414, 211142.1114734543),
(141990.4595356183, 211217.495767633),
(142284.34299131297, 210912.16739904383),
(142032.31566415634, 211146.46056591507),
(643671.0030674124, 155539.34763368565),
(643524.3952980377, 155623.166977987),
(709067.530365265, 106617.37499372978)]

# switch positions of coordinates
for i in range(len(points_no)):
    points_no[i] = [points_no[i][1], points_no[i][0]]

# state how many oil rigs Denmark operates
print("Norway operates", len(points_no), "oil rigs")
# visualize graph
Graph = create_Graph(points_no, 9999999999)
visualize_Graph(Graph)

speed= 150
# make an empty list with the dimensions of the points list
points1 = [[0,0] for i in range(len(points_no))]

 # devide al coordinates by the speed to get the time in hours instead of km
for i in range(len(points_no)):
    points1[i][0] = points_no[i][0]/(1000 * speed)
    points1[i][1] = points_no[i][1]/(1000 * speed)

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
plt.ylim(0, 15)
plt.xlim(0, 5)
# plt.title("Minimum dominating set size as a function of the maximum time")
plt.show()

print(min_set_size)