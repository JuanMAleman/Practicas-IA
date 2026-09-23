from ..s3 import GeneticAlgorithm
import networkx as nx
import logging


EDGES = {
    "A": (("B", 29), ("C", 20), ("D", 21), ("E", 50), ("F", 31)),
    "B": (("A", 29), ("C", 50), ("D", 29), ("E", 55), ("F", 40)),
    "C": (("A", 20), ("B", 50), ("D", 15), ("E", 14), ("F", 25)),
    "D": (("A", 21), ("B", 29), ("C", 15), ("E", 19), ("F", 36)),
    "E": (("A", 50), ("B", 55), ("C", 14), ("D", 19), ("F", 27)),
    "F": (("A", 31), ("B", 40), ("C", 25), ("D", 36), ("E", 27)),
}

G = nx.MultiDiGraph()
for k, nodes in EDGES.items():
    for dst, units in nodes:
        G.add_edge(k, dst, length=units)


def test_genetic_algorithm_init_population():
    inst = GeneticAlgorithm(G, 50, 50, 15)
    inst._init_population()
    assert len(inst._population) == 50


def test_genetic_algorithm_calculate_distance():
    inst = GeneticAlgorithm(G, 50, 50, 15)
    assert inst._calculate_distance("D E C F A B D".split(" ")) == 147


def test_genetic_algorithm_mutate():
    inst = GeneticAlgorithm(G, 50, 50, 15)
    path = "D E C F A B D".split(" ")
    for p, d in zip(inst._mutate(path), path):  # Hay una pequeña posibilidad de que esta prueba falle
        assert p == d


def test_genetic_algorithm():
    inst = GeneticAlgorithm(G, 50, 50, 15)
    path, total_distance = inst.find_optima()
    logging.info(inst.report(total_nodes=len(G)))

    # La misma ruta en cualquier sentido es óptima
    # B → A → D → C → E → F
    # F → E → C → D → A → B
    assert total_distance == 106
