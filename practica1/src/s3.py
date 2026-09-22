# https://antonio-richaud.com/biblioteca/archivo/Algoritmos-geneticos/algoritmos-geneticos.pdf
from typing import Union, Optional
from .metrics import Metrics
from . import find_property
from networkx import Graph
from enum import Enum
import random


class BreedingMethod(Enum):
    CROSSOVER = 0
    MUTATION = 1


class GeneticAlgorithm(Metrics):
    def __init__(self, g: Graph, bm: BreedingMethod, initial_population: int, mutation_rate: float = -1):
        super().__init__("Algoritmo genético")

        if initial_population < 0:
            raise ValueError("Tamaño de población inicial negativo")
        if mutation_rate != -1 and bm != BreedingMethod.MUTATION:
            raise ValueError("mutation_rate no puede utilizarse con crossover")
        if mutation_rate != -1 and 0 <= mutation_rate >= 1:
            raise ValueError("mutation_rate fuera del rango (0, 1)")

        self._g = g
        self._bm = bm
        self._initial_population = initial_population
        self._mutation_rate = mutation_rate
        self._initial_population = []

    def _init_population(self):
        for _ in range(self._initial_population):
            path = list(self._g.nodes.keys())
            random.shuffle(path)
            self._initial_population.append(path)

    def _get_distance(self, path: list) -> float:
        distance = 0
        adjacent_nodes = None
        for p in path:
            if adjacent_nodes is None:
                adjacent_nodes = self._g[p]
                continue

            distance += find_property(dict(adjacent_nodes[p]), "length")
            adjacent_nodes = self._g[p]

        return distance

    def _mutate(self, path: list) -> list:
        path_len = len(path)
        for i in range(path_len):
            if random.random() < self._mutation_rate:
                s = random.randint(0, path_len)
                path[i], path[s] = path[s], path[i]
        return path

    def _crossover(self, parent_a: list, parent_b: list) -> list:
        r = random.Random()
        child = [None] * len(self._g)
        start, end = r.randint(0, len(child)), r.randint(0, len(child))
        if start > end:
            start, end = end, start

        parent_a_part = parent_a[start:end]
        parent_b_part = [part for part in parent_b if part not in parent_a_part]
        child[start:end] = parent_a_part

        return [part if part is not None else parent_b_part.pop(0) for part in child]

    def _breed(self, path_a: list, path_b: Optional[list] = None) -> list:
        if self._bm == BreedingMethod.MUTATION:
            if path_b is not None:
                raise ValueError("Solo se puede utilizar una ruta para realizar mutación")
            return self._mutate(path_a)

        if path_b is None:
            raise ValueError("Para realizar crossover, se necesitan dos rutas")
        return self._crossover(path_a, path_b)

    def _fitness(self):
        ...

    def _choice(self):
        ...

    def perform_search(self, start_node: Union[int, str], end_node: Union[int, str])\
            -> tuple[list[str], Union[str, float]]:
        if start_node not in self._g or end_node not in self._g:
            raise ValueError(f"Nodo de inicio/fin no encontrado(s): {start_node}/{end_node}")
        ...


def run(**kwargs):
    ...
