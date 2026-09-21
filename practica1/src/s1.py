from .map_download import fetch_graph
from queue import Queue, LifoQueue
from .metrics import Metrics
from . import find_property
from networkx import Graph
from typing import Union
from osmnx import plot
from enum import Enum
import random
import heapq


class Algorithm(Enum):
    BFS = 0
    DFS = 1
    UCS = 2


class UFSA(Metrics):  # "Uninformed Search Algorithms"
    def __init__(self, g: Graph, algorithm: Algorithm):
        super().__init__(algorithm.name)
        self._g = g
        self._chosen_algorithm = algorithm
        self._data_structure: Union[Queue, LifoQueue, list, None] = None
        
    def _init_data_structure(self, start_node: str):
        if self._chosen_algorithm == Algorithm.BFS:
            self._data_structure = Queue()
        elif self._chosen_algorithm == Algorithm.DFS:
            self._data_structure = LifoQueue()
        else:
            self._data_structure = []

        # La estructura se llena con cuádruplas. La distancia acumulada se coloca primero porque es el parámetro
        # que utiliza heapq para dar prioridad a un elemento u otro de acuerdo con la documentación, que es
        # lo que utiliza UCS, https://docs.python.org/3/library/heapq.html#basic-examples
        #                      distance weight    node         path
        self._data_structure_put((0,      0,   start_node, [start_node]))
        self._path = []
    
    def _data_structure_size(self) -> int:
        if isinstance(self._data_structure, list):
            return len(self._data_structure)
        return self._data_structure.qsize()
    
    def _data_structure_get(self) -> tuple:
        if isinstance(self._data_structure, list):
            return heapq.heappop(self._data_structure)
        return self._data_structure.get()

    def _data_structure_put(self, data: tuple[float, float, str, list]):
        if isinstance(self._data_structure, list):
            return heapq.heappush(self._data_structure, data)
        return self._data_structure.put(data)

    def perform_search(self, start_node: str, end_node: str) -> tuple[list[str], float]:
        if start_node not in self._g or end_node not in self._g:
            raise ValueError(f"Nodo de inicio/fin no encontrado(s): {start_node}/{end_node}")

        self.reset_metrics()
        self._start_timer()

        self._init_data_structure(start_node)

        while self._data_structure_size():
            if self._data_structure_size() > self._max_elements_in_structure:
                self._max_elements_in_structure = self._data_structure_size()

            total_distance, weight, current_node, path_to_current = self._data_structure_get()
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

                self._data_structure_put((
                    total_distance + weight, find_property(properties, "length"), adjacent_node,
                    path_to_current.copy() + [adjacent_node]
                ))

        self._end_timer()
        return self._path, self._total_distance


def run(**kwargs):
    draw = False
    if "draw" in kwargs:
        draw = kwargs.pop("draw")

    start_node, end_node = None, None
    if "start_node" in kwargs:
        start_node = kwargs.pop("start_node")
    if "end_node" in kwargs:
        end_node = kwargs.pop("end_node")

    g = fetch_graph(*kwargs)
    nodes = list(g.nodes.keys())

    if start_node is None:
        start_node = random.choice(nodes)
    if end_node is None:
        end_node = random.choice(nodes)

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

    bfs = UFSA(g, Algorithm.BFS)
    bfs.perform_search(start_node, end_node)
    print(bfs.report(start_node, end_node, len(nodes)), "\n")

    dfs = UFSA(g, Algorithm.DFS)
    dfs.perform_search(start_node, end_node)
    print(dfs.report(start_node, end_node, len(nodes)), "\n")

    ucs = UFSA(g, Algorithm.UCS)
    ucs.perform_search(start_node, end_node)
    print(ucs.report(start_node, end_node, len(nodes)), "\n")

    if draw:
        plot.plot_graph(g)
