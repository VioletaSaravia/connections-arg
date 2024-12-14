from neo4j import GraphDatabase
import matplotlib

matplotlib.use("tkAgg")

import matplotlib.pyplot as plt
import networkx as nx
from dataclasses import dataclass


@dataclass
class ConnectionsGraph:
    nodes: set = set()
    edges: list[dict] = []
    categories: list[str] = []


def extract() -> ConnectionsGraph:
    result = ConnectionsGraph()

    with open("data/conecciones.txt", "r", encoding="utf-8") as file:
        lines: list[str] = [line.strip() for line in file if line.strip()]

    cur_edge: str = ""
    cur_diff: int = 1
    first_word: str = ""
    for i in range(len(lines) - 1):
        line: str = lines[i]

        # This line is empty
        if line == "\n":
            continue

        # This line is a title
        if line[0] == "#":
            cur_edge = line[4:]
            cur_diff = int(line[2])
            result.categories += cur_edge
            continue

        # This line is the first word of the group
        # (needed to join ending with beggining)
        if lines[i - 1][0] == "#":
            first_word = line

        # This line is the last word of the group
        # (i.e. join with beggining word)
        to_node = lines[i + 1] if lines[i + 1][0] != "#" else first_word

        result.nodes.add(line)

        result.edges.append(
            {
                "from": line,
                "to": to_node,
                "difficulty": cur_diff,
                "name": cur_edge,
            }
        )

    return result


def view(graph: ConnectionsGraph):
    g: nx.Graph = nx.Graph()

    for edge in graph.edges:
        g.add_edge(edge["from"], edge["to"])

    pos = nx.spring_layout(g)

    # pos_cycles = {t: [pos[x] for x in data[t]] for t in data.keys()}
    # pos_cycles_centers = {t: [0, 0] for t in data.keys()}

    # for k, v in pos_cycles.items():
    #    for n in v:
    #        pos_cycles_centers[k][0] += n[0]
    #        pos_cycles_centers[k][1] += n[1]
    #
    #    # TODO This is the average. We may want the mean.
    #    pos_cycles_centers[k][0] /= len(v)
    #    pos_cycles_centers[k][1] /= len(v)
    #
    # E = nx.Graph()
    #
    # for n in pos_cycles_centers.keys():
    #    E.add_node(n)

    nx.draw_networkx(g, pos)
    # nx.draw_networkx(
    #    E,
    #    pos=pos_cycles_centers,
    #    **{
    #        'node_color':'red'
    #    }
    # )

    plt.show()


def load(graph: ConnectionsGraph):
    def build(tx, nodes, edges):
        for node in nodes:
            tx.run("MERGE (n:Node {name: $name})", name=node)

        for edge in edges:
            tx.run(
                """
                MATCH (a:Node {name: $from}), (b:Node {name: $to})
                MERGE (a)-[r:$name {difficulty: $difficulty}]->(b)
            """,
                **edge
            )

    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

    with driver.session() as session:
        session.write_transaction(build, graph.nodes, graph.edges)


graph = extract()

view(graph)

load(graph)
