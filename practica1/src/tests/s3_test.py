from ..s3 import GeneticAlgorithm, BreedingMethod
import networkx as nx
import logging


EDGES = {
    "A": (("B", 29), ("C", 20), ("D", 21), ("E", 50), ("F", 31)),
    "B": (("C", 50), ("D", 29), ("E", 55), ("F", 40)),
    "C": (("D", 15), ("E", 14), ("F", 25)),
    "D": (("E", 19), ("F", 36),),
    "E": (("F", 27),)
}

G = nx.MultiDiGraph()
for k, nodes in EDGES.items():
    for dst, units in nodes:
        G.add_edge(k, dst, length=units)


def test_genetic_algorithm_mutation_s_g():
    inst = GeneticAlgorithm(G, BreedingMethod.MUTATION)
    sn, en = "F", "E"
    path, total_distance = inst.perform_search(sn, en)
    logging.debug(inst.report(sn, en, len(G)))
    for p, d in zip(path, "F → A → B → D → C → E".split(" → ")):
        assert p == d
    assert total_distance == 145
