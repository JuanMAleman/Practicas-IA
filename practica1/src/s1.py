from .map_download import download
from queue import Queue, LifoQueue
from .metrics import Metrics
from networkx import Graph
from osmnx import plot
import heapq


class BFS(Metrics):
    def __init__(self, g: Graph):
        super().__init__("BFS")
        self._g = g
        self._queue = Queue()

    def perform_search(self, start_node: str, end_node: str) -> tuple[list[str], float]:
        ...


class DFS(Metrics):
    def __init__(self, g: Graph):
        super().__init__("DFS")
        self._g = g
        self._stack = LifoQueue()

    def perform_search(self, start_node: str, end_node: str) -> tuple[list[str], float]:
        ...


class UCS(Metrics):
    def __init__(self, g: Graph):
        super().__init__("UCS")
        self._g = g
        self._queue = []

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
