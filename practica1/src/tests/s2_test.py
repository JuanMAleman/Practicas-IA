import matplotlib.pyplot as plt
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
for k, city in EDGES.items():
    for dst, km in city:
        G.add_edge(k, dst, weight=km)


def draw_graph():
    # https://networkx.org/documentation/stable/auto_examples/drawing/plot_weighted_graph.html
    # https://matplotlib.org/stable/gallery/shapes_and_collections/fancybox_demo.html

    pos = nx.spring_layout(G, seed=5)
    nx.draw_networkx_nodes(G, pos, node_size=2500, node_color="#E3E8EF", linewidths=2, edgecolors="#97A2B6")

    nx.draw_networkx_edges(G, pos, width=3, edge_color="#CDD5E0")
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight=700)
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels, bbox={"boxstyle": "round,pad=0.3", "fc": "#FFF"})

    ax = plt.gca()
    ax.margins(0.05)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def test_astar_s_g():
    path, total_distance = AStar(G, lambda _: _).perform_search("S", "G")
    for p, d in zip(path, "S → A → C → G".split(" → ")):
        assert p == d
    assert total_distance == 10
