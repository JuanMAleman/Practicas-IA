from .map_download import download
from queue import Queue, LifoQueue
from .metrics import Metrics
from networkx import Graph
from . import find_property
from osmnx import plot
from enum import Enum
import heapq


class Algorithm(Enum):
    BFS = 0
    DFS = 1


class FS(Metrics):
    def __init__(self, g: Graph, algorithm: Algorithm):
        super().__init__(algorithm.name)
        self._g = g
        self._algorithm = algorithm
        self._data_structure = Queue() if algorithm == Algorithm.BFS else LifoQueue()

    def perform_search(self, start_node: str, end_node: str) -> tuple[list[str], float]:
        if start_node not in self._g or end_node not in self._g:
            raise ValueError(f"Nodo de inicio/fin no encontrado(s): {start_node}/{end_node}")

        self.reset_metrics()
        self.start_timer()

        self._data_structure = Queue() if self._algorithm == Algorithm.BFS else LifoQueue()

        # La estructura se llena una tupla de 4 (cuatrupla?) elementos,
        #                            node   weight distance     path
        self._data_structure.put((start_node, 0,      0,    [start_node]))
        self._path = []

        while not self._data_structure.empty():
            if self._data_structure.qsize() > self._max_elements_in_structure:
                self._max_elements_in_structure = self._data_structure.qsize()

            current_node, weight, total_distance, path_to_current = self._data_structure.get()
            self._explored_nodes += 1

            if current_node == end_node:
                self._path = path_to_current
                self._total_edges = len(self._path) - 1
                self._total_distance = weight + total_distance
                break

            adjacent_nodes = self._g[current_node]
            for adjacent_node, properties in adjacent_nodes.items():
                if adjacent_node in path_to_current:
                    continue

                self._data_structure.put((
                    adjacent_node, find_property(properties), total_distance + weight,
                    path_to_current.copy() + [adjacent_node]
                ))

        return self._path, self._total_distance


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

    # print(g[919822045])
    #   {8085857839: {0: {'osmid': 359868763, 'highway': 'residential', 'lanes': '2', 'name': 'Calle Margarita Maza de
    #   Juárez', 'oneway': True, 'reversed': False, 'length': np.float64(18.088914899282003)}}, 8085857838: {0: {
    #   'osmid': 881119990, 'highway': 'residential', 'name': 'Calle Sindicato Nacional', 'oneway': False, 'reversed':
    #   False, 'length': np.float64(15.22960558200053)}}, 8085857840: {0: {'osmid': 881119990, 'highway':
    #   'residential', 'name': 'Calle Sindicato Nacional', 'oneway': False, 'reversed': True, 'length': np.float64(
    #   5.898320019204013)}}}
    #
    # Los grafos MultiDiGraph tienen la propiedad 0 que hace referencia a sus propios datos y los nodos con los que
    # conectan en un dict

    ...

    if draw:
        plot.plot_graph(g)
