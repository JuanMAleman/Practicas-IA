from ..s3 import GeneticAlgorithm, BreedingMethod
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


def test_genetic_algorithm_mutation_s_g():
    inst = GeneticAlgorithm(G, BreedingMethod.CROSSOVER, 3)
    sn, en = "F", "E"
    path, total_distance = inst.perform_search(sn, en)
    logging.debug(inst.report(sn, en, len(G)))
    for p, d in zip(path, "F → A → B → D → C → E".split(" → ")):
        assert p == d
    assert total_distance == 145
