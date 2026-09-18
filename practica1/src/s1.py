from .map_download import download
from networkx import Graph
from typing import Optional
from queue import Queue


class BFS:
    def __init__(self, g: Graph):
        self._g = g

    def perform_search(self, start_node: str, end_node: str) -> tuple[list[str], float]:
        ...


def run(**kwargs):
    g = download(*kwargs)
    ...
