from networkx.classes import MultiDiGraph
from .map_download import fetch_graph
from typing import Union, Optional
from queue import Queue, LifoQueue
from .metrics import Metrics
from . import find_property
from networkx import Graph
from osmnx import plot
import multiprocessing
from enum import Enum
import logging
import random
import heapq
import re


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
        self.frontier_snapshots = []

        self._explored_nodes = 0
        self._total_distance = 0
        self._total_edges = 0
        self._max_elements_in_structure = 0
        self._path = []

    def _init_data_structure(self, start_node: Union[int, str]):
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

    def frontier(self) -> list[Union[int, str]]:
        if isinstance(self._data_structure, list):
            return [v[2] for v in self._data_structure]
        return [v[2] for v in list(self._data_structure.queue)]

    def perform_search(self, start_node: Union[int, str], end_node: Union[int, str])\
            -> tuple[list[str], Union[str, float]]:
        if start_node not in self._g or end_node not in self._g:
            raise ValueError(f"Nodo de inicio/fin no encontrado(s): {start_node}/{end_node}")

        r = random.Random()
        self.reset_metrics()
        self._start_timer()

        self._init_data_structure(start_node)

        while self._data_structure_size():
            if self._is_timeout:
                self.frontier_snapshots.append(self.frontier())
                self._path = []
                self._total_distance = "No termino,"
                self._total_edges = f"timeout de {self._timeout}s"
                break

            if self._data_structure_size() > self._max_elements_in_structure:
                self._max_elements_in_structure = self._data_structure_size()
                if len(self.frontier_snapshots) < 2 and r.randint(1, 11) % 2 == 0:
                    self.frontier_snapshots.append(self.frontier())

            total_distance, weight, current_node, path_to_current = self._data_structure_get()
            self._explored_nodes += 1

            if current_node == end_node:
                self.frontier_snapshots.append(self.frontier())
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

    def report_with_nodes(self, start_node: str = "", end_node: str = "", total_nodes: int = 0) -> str:
        report = "\n".join(super().report(total_nodes).split("\n")[1:])
        return (f"Reporte de {self._algorithm}\n"
                f"  Nodo inicial:     {start_node if start_node else 'sin especificar'}\n"
                f"  Nodo final:       {end_node if end_node else 'sin especificar'}\n"
                f"  Nodos expandidos: {self._explored_nodes}\n"
                f"    Tamaño de\n"
                f"  frontera máximo:  {self._max_elements_in_structure}\n"   # Máximos nodos en la estructura de datos
                f"{report}")


def plot_graph(g: MultiDiGraph, start_node, end_node, frontier: Optional[list] = None):
    nc = []
    for n in g.nodes:
        if n == start_node:
            nc.append("#00FF00")
        elif n == end_node:
            nc.append("#0000FF")
        elif not frontier or n not in frontier:
            nc.append("#111111")
        else:
            nc.append("#E9A23B")

    ns = [180 if n in [start_node, end_node] else 90 if frontier and n in frontier else 15 for n in g.nodes]
    plot.plot_graph(g, bgcolor="w", node_color=nc, node_size=ns, edge_color="#666666")


def run(**kwargs):
    show_graph = False

    if "show_graph" in kwargs:
        show_graph = kwargs.pop("show_graph")

    def plot_snapshots(ufsa: UFSA):
        if show_graph:
            for snapshot in ufsa.frontier_snapshots[:-1]:
                multiprocessing.Process(target=plot_graph, args=(g, start_node, end_node, snapshot)).start()
            plot_graph(g, start_node, end_node, ufsa.frontier_snapshots[-1])

    start_node, end_node = None, None
    if "start_node" in kwargs:
        start_node = kwargs.pop("start_node")
    if "end_node" in kwargs:
        end_node = kwargs.pop("end_node")

    if start_node is not None and re.match(r"^\d+$", start_node):
        start_node = int(start_node)
    if end_node is not None and re.match(r"^\d+$", end_node):
        end_node = int(end_node)

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

    logging.info(f"Nodo inicial: {start_node}")
    logging.info(f"Nodo final:   {end_node}")

    bfs = UFSA(g, Algorithm.BFS)
    bfs.perform_search(start_node, end_node)
    print(bfs.report_with_nodes(start_node, end_node, len(nodes)), "\n")
    plot_snapshots(bfs)

    dfs = UFSA(g, Algorithm.DFS)
    dfs.perform_search(start_node, end_node)
    print(dfs.report_with_nodes(start_node, end_node, len(nodes)), "\n")
    plot_snapshots(dfs)

    ucs = UFSA(g, Algorithm.UCS)
    ucs.perform_search(start_node, end_node)
    print(ucs.report_with_nodes(start_node, end_node, len(nodes)), "\n")
    plot_snapshots(ucs)
