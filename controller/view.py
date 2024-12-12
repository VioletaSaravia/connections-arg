import matplotlib
matplotlib.use('tkAgg')
import matplotlib.pyplot as plt
import networkx as nx
import json

with open("conecciones.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

# LOAD NODES
G = nx.Graph()

for k, v in data.items():
    for n in range(len(v) - 1):
        G.add_edge(v[n], v[n + 1])
    G.add_edge(v[-1], v[0])

pos = nx.spring_layout(G)

# LOAD EDGES
pos_cycles = {t: [pos[x] for x in data[t]] for t in data.keys()}
pos_cycles_centers = {t: [0, 0] for t in data.keys()}

for k, v in pos_cycles.items():
    for n in v:
        pos_cycles_centers[k][0] += n[0]  
        pos_cycles_centers[k][1] += n[1]  

    # TODO This is the average. We may want the mean.
    pos_cycles_centers[k][0] /= len(v)
    pos_cycles_centers[k][1] /= len(v) 

E = nx.Graph()

for n in pos_cycles_centers.keys():
    E.add_node(n)

nx.draw_networkx(G, pos)
nx.draw_networkx(
    E,
    pos=pos_cycles_centers,
    **{
        'node_color':'red'
    }
)

plt.show()
