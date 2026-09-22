# https://antonio-richaud.com/biblioteca/archivo/Algoritmos-geneticos/algoritmos-geneticos.pdf
from .metrics import Metrics
from networkx import Graph
from typing import Union
from enum import Enum


class BreedingMethod(Enum):
    CROSSOVER = 0
    MUTATION = 1


class GeneticAlgorithm(Metrics):
    def __init__(self, g: Graph, bm: BreedingMethod):
        super().__init__("Algoritmo genético")
        self._g = g
        self._bm = bm

    def init_population(self):
        ...

    def fitness(self):
        ...

    def choice(self):
        ...

    def perform_search(self, start_node: Union[int, str], end_node: Union[int, str])\
            -> tuple[list[str], Union[str, float]]:
        ...


def run(**kwargs):
    ...
