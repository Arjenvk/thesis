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
points_dk = [
(64172.79213556182, 124797.84441804112),
(52179.67547545768, 182264.59093855572),
(52213.29396167677, 182319.69240863965),
(52280.308295134455, 182454.93149142695),
(52179.564155966975, 182377.69988462474),
(53508.83019552939, 180436.20746056963),
(53407.64077839814, 179558.97105676745),
(53310.458862936124, 179436.92551360425),
(53234.09369225148, 179264.6985943757),
(53353.650825363584, 179298.8980664906),
(53470.313651714474, 179647.71126175398),
(53129.78732937761, 179451.34297078563),
(64465.67371583916, 140391.10779694765),
(64401.776328123175, 140365.304082878),
(64525.340962904505, 140484.82785292395),
(64458.549268427305, 140636.18766014726),
(64648.68295870349, 140614.6286435732),
(64386.97083584778, 140301.07409627753),
(44755.444675982, 176203.24126472528),
(67458.05294785276, 110641.49427734088),
(59080.92730718665, 157203.80824895768),
(59112.319403590634, 157277.99648796505),
(59170.87345574796, 157028.84049573593),
(131175.88232454285, 75792.57633220428),
(92874.74172475468, 118456.11803573678),
(59012.131861876696, 168087.48092567903),
(165051.8505263161, 157515.9803434477),
(182653.57709105778, 203337.39690131234),
(156082.72783361096, 140588.26633100578),
(186434.6549153421, 213546.2874618583),
(120041.70685539953, 81322.78114035417),
(59888.99549085554, 170895.9277868283),
(59110.42697224673, 167927.90824660385),
(59133.58142633177, 168143.8007779299),
(53030.37902410049, 179591.829507761),
(92814.29524125438, 118510.05621186749),
(89506.99316978548, 118770.70207119483),
(59924.50640841853, 170977.39358226204),
(59965.47198103089, 171163.6812791188),
(59779.45711191464, 170767.52715046034),
(165974.13250753842, 160646.71210657124),
(121612.64750947338, 84368.03259758255),
(121977.21884182189, 80249.19402178883),
(120027.7919190498, 81546.80957662594),
(138790.91473123804, 51188.59928350325),
(98168.98538739234, 56113.121654213464)]
points_combined = [(286811.77372210845, 570319.0545376585),
(274818.6570620043, 627785.8010581731),
(274852.2755482234, 627840.902528257),
(274919.2898816811, 627976.1416110443),
(274818.5457425136, 627898.9100042421),
(276147.811782076, 625957.417580187),
(276046.6223649448, 625080.1811763848),
(275949.44044948276, 624958.1356332216),
(275873.0752787981, 624785.908713993),
(275992.6324119102, 624820.108186108),
(276109.2952382611, 625168.9213813713),
(275768.76891592424, 624972.553090403),
(287104.6553023858, 585912.317916565),
(287040.7579146698, 585886.5142024953),
(287164.32254945114, 586006.0379725413),
(287097.53085497394, 586157.3977797646),
(287287.6645452501, 586135.8387631905),
(287025.9524223944, 585822.2842158949),
(267394.42626252864, 621724.4513843426),
(290097.0345343994, 556162.7043969582),
(281719.9088937333, 602725.018368575),
(281751.3009901373, 602799.2066075824),
(281809.8550422946, 602550.0506153533),
(353814.8639110895, 521313.7864518217),
(315513.7233113013, 563977.3281553541),
(281651.11344842333, 613608.6910452964),
(387690.8321128627, 603037.190463065),
(405292.5586776044, 648858.6070209297),
(378721.7094201576, 586109.4764506231),
(409073.63650188874, 659067.4975814756),
(342680.6884419462, 526843.9912599715),
(282527.9770774022, 616417.1379064457),
(281749.40855879337, 613449.1183662212),
(281772.5630128784, 613665.0108975472),
(275669.3606106471, 625113.0396273783),
(315453.276827801, 564031.2663314849),
(312145.9747563321, 564291.9121908122),
(282563.48799496517, 616498.6037018794),
(282604.4535675775, 616684.8913987362),
(282418.4386984613, 616288.7372700777),
(388613.11409408506, 606167.9222261886),
(344251.62909602, 529889.2427172),
(344616.2004283685, 525770.4041414062),
(342666.77350559644, 527068.0196962433),
(361429.8963177847, 496709.80940312066),
(320807.966973939, 501634.3317738308),
(391883.4580946099, 414455.0342854818),
(405433.6004724391, 426224.0192767986),
(394685.035719404, 413772.68282208755),
(353535.00671123527, 440907.7529880651),
(364781.0582686262, 433834.3316537081),
(385629.64042133465, 401255.26236798207),
(394799.8061144119, 413370.63255377964),
(394774.0913120387, 413693.63289283577),
(718060.8093874715, 319037.4809413939),
(731029.0847869255, 277989.2236986697),
(689181.8618079182, 321324.16733412154),
(839576.1636619922, 394802.3592258553),
(395059.18052795995, 413308.97605199635),
(749582.1477199858, 340303.42691625),
(396819.3643163834, 412317.45934895915),
(394926.82165340707, 413524.82970172155),
(394869.9373936113, 413636.3245158548),
(394798.5816000132, 414279.31724226207),
(396869.45808724035, 412586.9396463855),
(394595.64616829716, 414475.660986693),
(394595.64616829716, 414475.660986693),
(394847.3395369807, 414018.5295682651),
(375838.0893306481, 419244.2093756498),
(380563.6017148234, 413957.876171954),
(380442.1521503674, 414075.28066140844),
(375638.27084467467, 419177.53215145983),
(375708.84740183875, 419258.7044296387),
(370978.7709185416, 417288.732257779),
(607887.3527519153, 267971.4467624617),
(927501.7521455688, 489600.61873691785),
(686246.8121136613, 332463.51086077665),
(910103.6289294874, 299221.66062199953),
(913088.3271166366, 300575.0728021554),
(914427.5005908795, 308659.7949995395),
(434621.4596389448, 399104.99891850783),
(635934.6324157529, 241204.22106728528),
(718532.3587504728, 321204.50652233826),
(833932.265478773, 370337.0627264143),
(834096.4617276918, 370441.719014258),
(846898.6484468821, 364572.18047474616),
(833799.0160482926, 370523.41562155564),
(822611.5185430599, 366954.670424358),
(857158.2979963543, 382363.17746996076),
(697470.3771339124, 328281.0346036535),
(565197.1072691297, 265969.49203503144),
(940520.6779133324, 294228.19987463305),
(948992.8703991361, 301709.70167805674),
(918961.988728853, 261874.09204559616),
(913532.3805654114, 259286.13722221393),
(923515.1785412794, 267295.0301094426),
(443285.6782463668, 385012.0732266377),
(565201.2260902897, 265970.7172151691),
(865383.5838515786, 445689.839853997),
(877846.1348043568, 457764.5330193159),
(529173.3408119902, 540877.2057460217),
(536057.7834006101, 560906.1503598132),
(457610.04768266436, 372588.47337257094),
(457646.2265171716, 372726.5686040637),
(457571.0858608857, 372438.3409527567),
(364848.74051902816, 433688.35832481633),
(369991.58967418596, 428927.6615892248),
(359232.2269305438, 438379.6769557351),
(364665.3973176908, 433800.8770917981),
(364629.44112216495, 433876.2613859768),
(364923.3245778596, 433570.93301738764),
(364671.297250703, 433805.2261842588),
(866309.984653959, 378198.1132520294),
(866163.3768845843, 378281.93259633076),
(931706.5119518116, 329276.1406120736),
(561977.8589148792, 170804.12106158468),
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

speed = 150 # km/h

# make an empty list with the dimensions of the points list
points1 = [[0,0] for i in range(len(points_dk))]
# devide al coordinates by the speed to get the time in hours instead of km
for i in range(len(points_dk)):
    points1[i][0] = points_dk[i][0]/(1000 * speed)
    points1[i][1] = points_dk[i][1]/(1000 * speed)


max_length = 0.5

Graph = create_Graph(points1, max_length)

min_dom_set = DSP_GREEDY(Graph)
print("Minimum dominating set: ", min_dom_set)
