from ..s1 import Algorithm, UFSA
import networkx as nx
import logging


EDGES = {
    "MEX": (("PUE", 130), ("CVA", 85), ("TOL", 70), ("QRO", 220)),
    "TOL": (("GDL", 350),),
    "QRO": (("GDL", 300),),
    "CVA": (("OAX", 320),),
    "PUE": (("VER", 220), ("OAX", 360)),
    "VER": (("OAX", 330),),
}

G = nx.Graph()
for k, city in EDGES.items():
    for dst, km in city:
        G.add_edge(k, dst, length=km)


def test_bfs_cdmx_oax():
    inst = UFSA(G, Algorithm.BFS)
    sn, en = "MEX", "OAX"
    path, total_distance = inst.perform_search(sn, en)
    logging.info(inst.report_with_nodes(sn, en, len(G)))
    for p, d in zip(path, "MEX → PUE → OAX".split(" → ")):  # La ruta es diferente a la de ejemplo
        assert p == d
    assert total_distance == 490


def test_bfs_tol_ver():
    inst = UFSA(G, Algorithm.BFS)
    sn, en = "TOL", "VER"
    path, total_distance = inst.perform_search(sn, en)
    logging.info(inst.report_with_nodes(sn, en, len(G)))
    for p, d in zip(path, "TOL → MEX → PUE → VER".split(" → ")):
        assert p == d
    assert total_distance == 420


def test_bfs_gdl_oax():
    inst = UFSA(G, Algorithm.BFS)
    sn, en = "GDL", "OAX"
    path, total_distance = inst.perform_search(sn, en)
    logging.info(inst.report_with_nodes(sn, en, len(G)))
    for p, d in zip(path, "GDL → TOL → MEX → PUE → OAX".split(" → ")):  # Pero el algoritmo funciona!
        assert p == d
    assert total_distance == 910


def test_bfs_ver_qro():
    inst = UFSA(G, Algorithm.BFS)
    sn, en = "VER", "QRO"
    path, total_distance = inst.perform_search(sn, en)
    logging.info(inst.report_with_nodes(sn, en, len(G)))
    for p, d in zip(path, "VER → PUE → MEX → QRO".split(" → ")):
        assert p == d
    assert total_distance == 570


def test_dfs_cdmx_oax():
    inst = UFSA(G, Algorithm.DFS)
    sn, en = "MEX", "OAX"
    path, total_distance = inst.perform_search(sn, en)
    logging.info(inst.report_with_nodes(sn, en, len(G)))
    for p, d in zip(path, "MEX → CVA → OAX".split(" → ")):
        assert p == d
    assert total_distance == 405


def test_dfs_tol_ver():
    inst = UFSA(G, Algorithm.DFS)
    sn, en = "TOL", "VER"
    path, total_distance = inst.perform_search(sn, en)
    logging.info(inst.report_with_nodes(sn, en, len(G)))
    for p, d in zip(path, "TOL → GDL → QRO → MEX → CVA → OAX → VER".split(" → ")):
        assert p == d
    assert total_distance == 1605


def test_dfs_gdl_oax():
    inst = UFSA(G, Algorithm.DFS)
    sn, en = "GDL", "OAX"
    path, total_distance = inst.perform_search(sn, en)
    logging.info(inst.report_with_nodes(sn, en, len(G)))
    for p, d in zip(path, "GDL → QRO → MEX → CVA → OAX".split(" → ")):
        assert p == d
    assert total_distance == 925


def test_dfs_ver_qro():
    inst = UFSA(G, Algorithm.DFS)
    sn, en = "VER", "QRO"
    path, total_distance = inst.perform_search(sn, en)
    logging.info(inst.report_with_nodes(sn, en, len(G)))
    for p, d in zip(path, "VER → OAX → PUE → MEX → QRO".split(" → ")):
        assert p == d
    assert total_distance == 1040


def test_ucs_cdmx_oax():
    inst = UFSA(G, Algorithm.UCS)
    sn, en = "MEX", "OAX"
    path, total_distance = inst.perform_search(sn, en)
    logging.info(inst.report_with_nodes(sn, en, len(G)))
    for p, d in zip(path, "MEX → CVA → OAX".split(" → ")):
        assert p == d
    assert total_distance == 405


def test_ucs_tol_ver():
    inst = UFSA(G, Algorithm.UCS)
    sn, en = "TOL", "VER"
    path, total_distance = inst.perform_search(sn, en)
    logging.info(inst.report_with_nodes(sn, en, len(G)))
    for p, d in zip(path, "TOL → MEX → PUE → VER".split(" → ")):
        assert p == d
    assert total_distance == 420


def test_ucs_gdl_oax():
    inst = UFSA(G, Algorithm.UCS)
    sn, en = "GDL", "OAX"
    path, total_distance = inst.perform_search(sn, en)
    logging.info(inst.report_with_nodes(sn, en, len(G)))
    for p, d in zip(path, "GDL → TOL → MEX → CVA → OAX".split(" → ")):
        assert p == d
    assert total_distance == 825


def test_ucs_ver_qro():
    inst = UFSA(G, Algorithm.UCS)
    sn, en = "VER", "QRO"
    path, total_distance = inst.perform_search(sn, en)
    logging.info(inst.report_with_nodes(sn, en, len(G)))
    for p, d in zip(path, "VER → PUE → MEX → QRO".split(" → ")):
        assert p == d
    assert total_distance == 570
