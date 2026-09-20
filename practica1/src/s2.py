from .map_download import download
from .metrics import Metrics
from typing import Callable
from networkx import Graph
from osmnx import plot
import heapq


class AStar(Metrics):
    def __init__(self, g: Graph, heuristics: Callable[[float], float]):
        super().__init__("A*")
        self._g = g
        self._queue = []
        self._h = heuristics

    def perform_search(self, start_node: str, end_node: str) -> tuple[list[str], float]:
        ...


def run(**kwargs):
    draw = False
    if "draw" in kwargs:
        draw = kwargs.pop("draw")

    g = download(*kwargs)
    ...

    if draw:
        plot.plot_graph(g)
