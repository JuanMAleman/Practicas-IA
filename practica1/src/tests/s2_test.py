from ..s2 import AStar
import networkx as nx


EDGES = {
    "S": (("A", 2), ("B", 6)),
    "A": (("C", 3), ("D", 8)),
    "B": (("D", 3),),
    "C": (("G", 5),),
    "D": (("G", 3),)
}

G = nx.DiGraph()  # TODO: Find how to specify direction
for k, nodes in EDGES.items():
    for dst, units in nodes:
        G.add_edge(k, dst, length=units)


def test_astar_s_g():
    path, total_distance = AStar(G, lambda _: _).perform_search("S", "G")
    for p, d in zip(path, "S → A → C → G".split(" → ")):
        assert p == d
    assert total_distance == 10
