import json
from neo4j import GraphDatabase

with open("conecciones.txt", 'r', encoding='utf-8') as file:
    lines: list[str] = [line.strip() for line in file if line.strip()]

nodes: set = set()
edges: list[dict] = []

cur_edge: str = ""
cur_diff: int = 1
first_word: str = ""
for i in range(len(lines) - 1):
    line: str = lines[i].strip()

    if line[0] == '#':
        cur_edge = line[4:]
        cur_diff = int(line[2])
        continue

    if lines[i - 1][0] == '#':
        first_word = line
    
    nodes.add(line)

    edges.append({
        "from": line, 
        "to": lines[i+1].strip() if lines[i+1][0] != '#' else first_word, 
        "difficulty": cur_diff, 
        "name": cur_edge
    })

uri = "bolt://localhost:7687"
username = "neo4j"
password = "password"

def load_graph(tx, nodes, edges):
    for node in nodes:
        tx.run("MERGE (n:Node {name: $name})", name=node)
    
    for edge in edges:
        tx.run("""
            MATCH (a:Node {name: $f}), (b:Node {name: $t})
            MERGE (a)-[r:$n {difficulty: $d}]->(b)
        """, f=edge['from'], t=edge['to'], d=edge['difficulty'], n=edge['name'])

driver = GraphDatabase.driver(uri, auth=(username, password))

with driver.session() as session:
    session.write_transaction(load_graph, nodes, edges)
