import matplotlib.pyplot as plt
from ..s1 import BFS, DFS, UCS
import networkx as nx


EDGES = {
        "MEX": (("PUE", 130), ("CVA", 85), ("TOL", 70), ("QRO", 200)),
        "TOL": (("GDL", 350),),
        "QRO": (("GDL", 300),),
        "CVA": (("OAX", 320),),
        "PUE": (("VER", 220), ("OAX", 360)),
        "VER": (("OAX", 330),),
    }

G = nx.Graph()
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


def test_bfs_cdmx_oax():
    path, total_distance = BFS(G).perform_search("MEX", "OAX")
    for p, d in zip(path, "MEX → CVA → OAX".split(" → ")):
        assert p == d
    assert total_distance == 405


def test_bfs_tol_ver():
    path, total_distance = BFS(G).perform_search("TOL", "VER")
    for p, d in zip(path, "TOL → MEX → PUE → VER".split(" → ")):
        assert p == d
    assert total_distance == 420


def test_bfs_gdl_oax():
    path, total_distance = BFS(G).perform_search("GDL", "OAX")
    for p, d in zip(path, "GDL → QRO → MEX → CVA → OAX".split(" → ")):
        assert p == d
    assert total_distance == 925


def test_bfs_ver_qro():
    path, total_distance = BFS(G).perform_search("VER", "QRO")
    for p, d in zip(path, "VER → PUE → MEX → QRO".split(" → ")):
        assert p == d
    assert total_distance == 570


def test_dfs_cdmx_oax():
    path, total_distance = DFS(G).perform_search("MEX", "OAX")
    for p, d in zip(path, "MEX → PUE → VER → OAX".split(" → ")):
        assert p == d
    assert total_distance == 680


def test_dfs_tol_ver():
    path, total_distance = DFS(G).perform_search("TOL", "VER")
    for p, d in zip(path, "TOL → GDL → QRO → MEX → PUE → VER".split(" → ")):
        assert p == d
    assert total_distance == 1220


def test_dfs_gdl_oax():
    path, total_distance = DFS(G).perform_search("GDL", "OAX")
    for p, d in zip(path, "GDL → TOL → MEX → PUE → VER → OAX → CVA".split(" → ")):
        assert p == d
    assert total_distance == 1420


def test_dfs_ver_qro():
    path, total_distance = DFS(G).perform_search("VER", "QRO")
    for p, d in zip(path, "VER → OAX → PUE → MEX → TOL → GDL → QRO".split(" → ")):
        assert p == d
    assert total_distance == 1540


def test_ucs_cdmx_oax():
    path, total_distance = UCS(G).perform_search("MEX", "OAX")
    for p, d in zip(path, "MEX → CVA → OAX".split(" → ")):
        assert p == d
    assert total_distance == 405


def test_ucs_tol_ver():
    path, total_distance = UCS(G).perform_search("TOL", "VER")
    for p, d in zip(path, "TOL → MEX → PUE → VER".split(" → ")):
        assert p == d
    assert total_distance == 420


def test_ucs_gdl_oax():
    path, total_distance = UCS(G).perform_search("GDL", "OAX")
    for p, d in zip(path, "GDL → TOL → MEX → CVA → OAX".split(" → ")):
        assert p == d
    assert total_distance == 825


def test_ucs_ver_qro():
    path, total_distance = UCS(G).perform_search("VER", "QRO")
    for p, d in zip(path, "VER → PUE → MEX → QRO".split(" → ")):
        assert p == d
    assert total_distance == 570
