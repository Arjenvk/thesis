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

points_uk = [(561977.8589148792, 170804.12106158468),
(582110.3227833156, 179078.83301760996),
(729623.7875351505, 229637.3168156476),
(727406.4145980394, 229253.1220040741),
(587352.5802437523, 167662.85497303517),
(545869.9285970926, 59218.55693419832),
(417386.1968378946, 198625.23838811766),
(92110.64473994914, 463584.0069219427),
(63671.63178801071, 466060.16334251815),
(357149.995855256, 414855.527446475),
(387113.5292336084, 293011.29932555294),
(589282.0809776718, 103930.26835522917),
(708090.924472535, 230565.2890924193),
(698753.2229458131, 228464.46668411916),
(898224.614747446, 212296.48390785532),
(578175.8467007168, 68241.23227541742),
(497748.96175595745, 116389.37992597674),
(599396.68123064, 145643.64904883027),
(454620.78539639246, 155011.21489561215),
(351428.84194542654, 396492.9182734564),
(896576.41836676, 241342.8725242236),
(385412.7900532689, 289916.952966153),
(385412.7900532689, 289916.952966153),
(525547.1083994005, 139690.17385484598),
(423148.53895931784, 148098.71749059833),
(780374.3433878031, 211019.04472037236),
(420898.9946893677, 290597.68658804183),
(797681.7412188882, 502653.9510966833),
(498811.1723371064, 215095.80369033944),
(498811.1723371064, 215186.44608389592),
(733495.5907444311, 173336.50462297013),
(743935.8005079692, 185223.6528304364),
(63708.81249793433, 467478.97814122133),
(63671.63178801071, 466059.8286924722),
(63677.86567949504, 464457.87183555646),
(84986.19732917938, 419402.20556535386),
(563131.0175200077, 176034.5795956894),
(869324.8504231144, 243106.14808367426),
(869418.2474758895, 249770.37546233702),
(561888.5806832621, 212004.51634494192),
(487017.87416297663, 209647.63071336356),
(378912.95630534086, 298674.0158454435),
(735859.9054093892, 224077.68894143443),
(728605.882111337, 226637.05040997645),
(633717.1481591491, 198377.7130993141),
(894452.1085239518, 245519.1626393499),
(606615.3049306199, 27428.957578753838),
(606660.2780048996, 27156.333449316906),
(384361.4887822177, 310464.2656137798),
(917334.4977734555, 183624.55648545158),
(63671.63178801071, 466044.3232415824),
(869418.2474758895, 248856.24389693586),
(937650.3048432283, 196181.72887954494),
(526757.9305007579, 163948.2376044904),
(528689.9915829664, 157528.57307358377),
(526202.0009637363, 149999.14490095765),
(525695.4972806266, 156199.1396939975),
(524995.4090030286, 170573.0955524558),
(388910.1144955214, 295569.42950474244),
(388808.3684809366, 295617.66495356744),
(465802.60560759436, 166810.23986845318),
(699024.5085448772, 224452.85535077416),
(885391.9264877792, 160305.46769097418),
(902430.0424706349, 201408.9385093912),
(497412.5542547805, 112672.59771638722),
(959586.7010599682, 201189.91598467794),
(637006.6391120907, 211713.4399320705),
(495447.5426032981, 210214.85808233882),
(948380.1679218104, 256532.6016613026),
(519068.9819521755, 183192.5502230386),
(886174.2798690749, 218470.52872940432),
(868911.1871953262, 217132.92690837625),
(607955.925558243, 83607.96737712236),
(602996.0856459485, 92862.96871906561),
(589127.4582049605, 78017.1249404835),
(588694.5367052648, 77800.71853378108),
(597768.6336777871, 63854.23655854682),
(930643.2994952453, 160859.02308972087),
(930968.9090058161, 231540.92792374216),
(612850.4209294422, 196516.65937225206),
(608577.422275342, 84572.67166872244),
(728662.4324126597, 226879.5915031468),
(902061.6862755995, 257593.11435642262),
(913516.2392392457, 250604.10078178137),
(920431.9626047779, 249865.70910040854),
(904470.8626953475, 181212.2320656347),
(921089.6381563852, 233332.30108168666),
(874613.1941527389, 219217.05886202335),
(392880.5467736451, 306258.65607234195),
(567905.6217996208, 215804.12919934015),
(487062.0680008223, 278130.57401931647),
(463248.3798913434, 311165.2483893668),
(932707.9420909872, 234682.57761983544),
(445432.58594580647, 196522.00401091954),
(590735.4682494681, 252696.33613538224),
(450941.00830872916, 155011.21489561215),
(446545.780853739, 203295.6348533215),
(856974.5095170541, 339433.15841873945),
(355016.44649471156, 363764.1698696562),
(535914.292576977, 164127.71053007795),
(535838.8179622199, 164311.4142959498),
(535999.6746264156, 163953.24770360655),
(355016.44649471156, 310216.71648787917),
(354490.68453969527, 366581.3064137234),
(563576.5181221617, 197749.93737379098),
(546591.0562584512, 121379.41005794387),
(95598.72966446634, 377064.43978904677),
(595945.2204185938, 151870.74565679638),
(545775.9749468621, 211007.35270645324),
(535838.8179622199, 164311.4142959498),
(944831.3025553199, 218686.11357405005),
(577149.4809956038, 387339.4342454993),
(274090.1823142525, 126748.65802566346),
(514129.0682287337, 246249.18645649776),
(864191.7973831454, 344351.63817570417),
(564448.2610545633, 173702.69693922717),
(565746.023678232, 173552.0559059049),
(354648.4242581492, 365720.12130409176),
(542026.9571359269, 167471.13330398843),
(10018.754171394743, 292763.6649102597),
(801382.3350513289, 486787.6872338898)]

# switch positions of coordinates
for i in range(len(points_uk)):
    points_uk[i] = [points_uk[i][1], points_uk[i][0]]

# state how many oil rigs Denmark operates
print("The UK operates", len(points_uk), "oil rigs")
# visualize graph
Graph = create_Graph(points_uk, 9999999999)
# visualize_Graph(Graph)

speed= 150
# make an empty list with the dimensions of the points list
points1 = [[0,0] for i in range(len(points_uk))]

 # devide al coordinates by the speed to get the time in hours instead of km
for i in range(len(points_uk)):
    points1[i][0] = points_uk[i][0]/(1000 * speed)
    points1[i][1] = points_uk[i][1]/(1000 * speed)

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
plt.xlabel("Maximum interdiction time (hours)")
plt.ylabel("Minimum dominating set size")
# set y axis limit
plt.ylim(0, 20)
plt.xlim(0, 5)
# only show integer on y axis
plt.yticks(range(0, 21, 2))
# plt.title("Minimum dominating set size as a function of the maximum time")
plt.show()

print(min_set_size)

dk = [46.0, 11.0, 6.0, 4.0, 3.0, 3.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
no = [69.0, 26.0, 17.0, 9.0, 8.0, 7.0, 6.0, 6.0, 6.0, 4.0, 4.0, 4.0, 4.0, 3.0, 3.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
uk = [121.0, 63.0, 37.0, 24.0, 17.0, 13.0, 13.0, 10.0, 10.0, 8.0, 7.0, 6.0, 6.0, 5.0, 4.0, 4.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

# sum the three lists
total = [dk[i] + no[i] + uk[i] for i in range(len(dk))]

plt.plot(max_times, dk, label = "Denmark")
plt.plot(max_times, no, label = "Norway")
plt.plot(max_times, uk, label = "United Kingdom")
plt.plot(max_times, total, label = "Total")
plt.xlabel("Maximum interdiction time (hours)")
plt.ylabel("Minimum dominating set size")
# set y axis limit
plt.ylim(0, 50)
plt.xlim(0, 5)
# only show integer on y axis
plt.yticks(range(0, 51, 10))
plt.xticks(range(0, 6, 1))
plt.legend()
# plt.title("Minimum dominating set size as a function of the maximum time")
plt.show()
