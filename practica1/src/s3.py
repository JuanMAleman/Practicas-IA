# https://antonio-richaud.com/biblioteca/archivo/Algoritmos-geneticos/algoritmos-geneticos.pdf
import matplotlib.pyplot as plt
from .metrics import Metrics
from . import find_property
from networkx import Graph
from typing import Union
import networkx as nx
import logging
import random


class GeneticAlgorithm(Metrics):
    def __init__(
        self, g: Graph, population_size: int, generations: int, best_sample_size: int, mutation_rate: float = 0.5
    ):
        super().__init__("Algoritmo genético")

        if population_size < 1:
            raise ValueError("Tamaño de población inicial menor que uno")
        if best_sample_size < 1:
            raise ValueError("Tamaño de muestra de los mejores individuos menor que uno")
        if population_size < best_sample_size:
            raise ValueError("Tamaño de muestra de los mejores individuos no puede ser "
                             "mayor que el tamaño de población")
        if mutation_rate != -1 and 0 <= mutation_rate >= 1:
            raise ValueError("mutation_rate fuera del rango (0, 1)")

        self._g = g
        self._population_size = population_size
        self._generations = generations
        self._best_sample_size = best_sample_size
        self._mutation_rate = mutation_rate
        self._population = []
        self._fittest_history = []

    def _init_population(self):
        for _ in range(self._population_size):
            path = list(self._g.nodes.keys())
            random.shuffle(path)
            # Los individuos se encuentran en la lista 'self._population' como tuplas con la distancia de la ruta como
            # primer valor
            self._population.append((self._calculate_distance(path), path))

    def _calculate_distance(self, path: list) -> float:
        distance = 0
        adjacent_nodes = None
        for p in path:
            if adjacent_nodes is None:
                adjacent_nodes = self._g[p]
                continue

            distance += find_property(adjacent_nodes[p], "length")
            adjacent_nodes = self._g[p]

        return distance

    def _mutate(self, path: list) -> list:
        path_len = len(path)
        for i in range(path_len):
            if random.random() < self._mutation_rate:
                s = random.randint(0, path_len - 1)
                path[i], path[s] = path[s], path[i]

        return path

    def _crossover(self, parent_a: list, parent_b: list) -> list:
        r = random.Random()
        child = [None] * len(self._g)
        start, end = r.randint(0, len(child) - 1), r.randint(0, len(child) - 1)
        if start > end:
            start, end = end, start

        parent_a_part = parent_a[start:end]
        parent_b_part = [part for part in parent_b if part not in parent_a_part]
        child[start:end] = parent_a_part

        return [part if part is not None else parent_b_part.pop(0) for part in child]

    def _sort_by_fitness(self):
        self._population.sort(key=lambda sample: sample[0])

    def _choice(self) -> list:
        return self._population[0:self._best_sample_size]

    def _evolve(self):
        self._sort_by_fitness()
        best = self._choice()
        offspring = []
        for _ in range(self._population_size - self._best_sample_size):
            parent_a, parent_b = random.choice(best), random.choice(best)

            child = self._crossover(parent_a[1], parent_b[1])
            child = self._mutate(child)
            child = (self._calculate_distance(child), child)
            offspring.append(child)

        self._population = best + offspring

    def find_optima(self) -> tuple[list[str], Union[str, float]]:
        self._start_timer()
        self._init_population()
        for _ in range(self._generations):
            self._evolve()
            self._fittest_history.append(self._population[0][0])

        self._path = self._population[0][1]
        self._total_distance = self._population[0][0]
        self._total_edges = len(self._path)
        self._end_timer()
        return self._population[0][1], self._population[0][0]

    @property
    def fittest_history(self):
        return self._fittest_history

    def report(self, total_nodes: int = 0) -> str:
        report = super().report(total_nodes)
        report += (f"\n    Tamaño de\n"
                   f"    población:       {self._population_size}\n"
                   f"  Generaciones:      {self._generations}\n"
                   f"    Cantidad de\n"
                   f"       mejores\n"
                   f"    seleccionados:   {self._best_sample_size}\n"
                   f"  Tasa de mutación:  {self._mutation_rate}")
        return report


def build_graph(**kwargs) -> tuple:
    with open("src/data/matrix_s3.txt", "r") as f:
        edges = eval(f.read())

    n = kwargs["nodes"]
    matrix = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(len(edges[i]) - (len(edges[0]) - n + 1)):
            col = i + 1 + j
            matrix[i][col] = edges[i][j]
            matrix[col][i] = edges[i][j]

    graph = False
    if "show_graph" in kwargs:
        graph = kwargs["show_graph"]
        logging.warning("Mostrar el grafo no esta soportado")
        logging.info("Mostrando matriz de distancias para creación del grafo")
        for k, line in enumerate(matrix):
            logging.info(" ".join([str(v).ljust(3, " ") for v in line]))

    nodes = [chr(i) for i in range(ord("A"), ord("A") + n)]
    g = nx.MultiDiGraph()

    for i, n0 in enumerate(nodes):
        for j, n1 in enumerate(nodes):
            if matrix[i][j] == 0:
                continue
            # TODO: Create graph without the matrix
            g.add_edge(n0, n1, length=matrix[i][j])

    return g, graph


def run(**kwargs):
    g, graph = build_graph(**kwargs)

    genetic_algorithm = GeneticAlgorithm(
        g, kwargs["population_size"], kwargs["generations"], kwargs["best_sample_size"], kwargs["mutation_rate"]
    )
    genetic_algorithm.find_optima()
    print(genetic_algorithm.report(total_nodes=len(g)))

    if not graph:
        return

    plt.plot(genetic_algorithm.fittest_history, marker="o", color="#0000FF")
    plt.title("Evolución de la mejor distancia por generación")
    plt.xlabel("Generación")
    plt.ylabel("Distancia")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
