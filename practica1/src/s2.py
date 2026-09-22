from .map_download import fetch_graph
from .metrics import Metrics
from typing import Callable
from networkx import Graph
from osmnx import plot


class AStar(Metrics):
    def __init__(self, g: Graph, heuristics: Callable[[float], float]):
        super().__init__("A*")
        self._g = g
        self._queue = []
        self._h = heuristics

    def perform_search(self, start_node: str, end_node: str) -> tuple[list[str], float]:
        ...


def run(**kwargs):
    show_graph = False
    if "show_graph" in kwargs:
        show_graph = kwargs.pop("show_graph")

    g = fetch_graph(*kwargs)
    ...

    if show_graph:
        plot.plot_graph(g)
