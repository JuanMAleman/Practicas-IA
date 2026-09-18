# https://osmnx.readthedocs.io/en/stable/user-reference.html
from networkx import MultiDiGraph
from osmnx import graph


def download(address: str = "Escuela Superior de Cómputo", dist: float = 1000) -> MultiDiGraph:
    return graph.graph_from_address(address=address, dist=dist, network_type="drive", retain_all=True)
