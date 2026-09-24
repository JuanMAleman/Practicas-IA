# https://antonio-richaud.com/biblioteca/archivo/Algoritmos-geneticos/algoritmos-geneticos.pdf
import matplotlib.pyplot as plt
from .metrics import Metrics
from . import find_property
from networkx import Graph
from typing import Union
import multiprocessing
import networkx as nx
import logging
import random
import math


def calculate_distance(g: Graph, path: list) -> float:
    distance = 0
    adjacent_nodes = None
    for p in path:
        if adjacent_nodes is None:
            adjacent_nodes = g[p]
            continue

        distance += find_property(adjacent_nodes[p], "length")
        adjacent_nodes = g[p]

    return distance


class GeneticAlgorithm(Metrics):
    def __init__(
        self, g: Graph, population_size: int, generations: int, best_sample_size: int, mutation_rate: float = 0.5
    ):
        super().__init__("Algoritmo genético")

        if population_size < 1:
            raise ValueError("Tamaño de población inicial menor que uno")
        if best_sample_size < 2:
            raise ValueError("Tamaño de muestra de los mejores individuos menor que dos")
        if population_size < best_sample_size:
            raise ValueError("Tamaño de muestra de los mejores individuos no puede ser "
                             "mayor que el tamaño de población")
        if 0 <= mutation_rate >= 1:
            raise ValueError("mutation_rate fuera del rango (0, 1)")

        self._g = g
        self._population_size = population_size
        self._generations = generations
        self._best_sample_size = best_sample_size
        self._mutation_rate = mutation_rate
        self._population = []
        self._fittest_history = []
        self._time_history = []
        self._improvement_history = []

    def _init_population(self):
        for _ in range(self._population_size):
            path = list(self._g.nodes.keys())
            random.shuffle(path)
            # Los individuos se encuentran en la lista 'self._population' como tuplas con la distancia de la ruta como
            # primer valor
            self._population.append((calculate_distance(self._g, path), path))

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
            child = (calculate_distance(self._g, child), child)
            offspring.append(child)

        self._population = best + offspring

    def find_optima(self) -> tuple[list[str], Union[str, float]]:
        self._fittest_history = []
        self._time_history = []
        self._improvement_history = []

        self._start_timer()
        self._init_population()
        for _ in range(self._generations):
            prev_fittest = self._population[0][0]
            self._evolve()

            self._fittest_history.append(self._population[0][0])
            self._time_history.append(self._raw_time)
            self._improvement_history.append((self._fittest_history[-1], prev_fittest))

        self._path = self._population[0][1]
        self._total_distance = self._population[0][0]
        self._total_edges = len(self._path)
        self._end_timer()
        return self._population[0][1], self._population[0][0]

    @property
    def fittest_history(self):
        return self._fittest_history

    @property
    def time_history(self):
        return self._time_history

    @property
    def improvement_history(self):
        return self._improvement_history

    def report(self, total_nodes: int = 0) -> str:
        report = super().report(total_nodes)
        report += (f"\n    Tamaño de\n"
                   f"    población:       {self._population_size}\n"
                   f"  Generaciones:      {self._generations}\n"
                   f"   Cantidad de\n"
                   f"     mejores\n"
                   f"   seleccionados:   {self._best_sample_size}\n"
                   f"  Tasa de mutación:  {self._mutation_rate}")
        return report


# https://optimization.cbe.cornell.edu/index.php?title=Simulated_annealing
class SimulatedAnnealing(Metrics):
    def __init__(
        self, g: Graph, initial_temperature: float = 1000, minimum_temperature: float = 50, cooling_rate: float = 0.7
    ):
        super().__init__("Recocido simulado")
        if initial_temperature < 100:
            raise ValueError("Temperatura inicial menor que 100")
        if minimum_temperature < 10:
            raise ValueError("Temperatura minima menor que 10")
        if 0 <= cooling_rate >= 1:
            raise ValueError("cooling_rate fuera del rango (0, 1)")

        self._g = g
        self._initial_temperature = initial_temperature
        self._alpha = cooling_rate
        self._minimum_temperature = minimum_temperature
        self._temperature = 0
        self._bests_history = []
        self._time_history = []
        self._improvement_history = []

    @property
    def bests_history(self):
        return self._bests_history

    @property
    def time_history(self):
        return self._time_history

    @property
    def improvement_history(self):
        return self._improvement_history

    @staticmethod
    def _generate_neighbor(current_solution: list) -> list:
        new_solution = current_solution.copy()
        i, s = random.sample(range(len(new_solution)), 2)
        new_solution[i], new_solution[s] = new_solution[s], new_solution[i]

        return new_solution

    def find_optima(self) -> tuple[list[str], Union[str, float]]:
        self._bests_history = []
        self._time_history = []
        self._improvement_history = []

        self._start_timer()
        current_solution = list(self._g.nodes.keys())
        self._temperature = self._initial_temperature

        while self._temperature > self._minimum_temperature:
            new_solution = self._generate_neighbor(current_solution)

            current_solution_distance = calculate_distance(self._g, current_solution)
            delta_e = calculate_distance(self._g, new_solution) - current_solution_distance
            if delta_e < 0 or random.random() < math.exp(-delta_e / self._temperature):
                current_solution = new_solution

            self._bests_history.append(current_solution_distance)
            self._time_history.append(self._raw_time)
            self._improvement_history.append((calculate_distance(self._g, current_solution), current_solution_distance))
            self._temperature *= self._alpha

        self._path = current_solution
        self._total_distance = calculate_distance(self._g, current_solution)
        self._total_edges = len(self._path)
        self._end_timer()
        return current_solution, self._total_distance

    def report(self, total_nodes: int = 0) -> str:
        report = super().report(total_nodes)
        report += (f"\n    Temperatura\n"
                   f"      inicial:      {self._initial_temperature}\n"
                   f"    Temperatura\n"
                   f"      minima:       {self._minimum_temperature}\n"
                   f"      Tasa de\n"
                   f"    enfriamiento:   {self._alpha}")
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

    graph = "show_graph" in kwargs and kwargs["show_graph"]
    if graph:
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


def graph_genetic(fittest_history):
    plt.plot(fittest_history, marker="o", color="#0000FF")
    plt.title("Algoritmo genético: evolución de la mejor distancia por generación")
    plt.xlabel("Generación (iteración)")
    plt.ylabel("Distancia")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def graph_costs(percentage_improvement: list, time_history: list, algorithm_name: str):
    plt.plot(time_history, percentage_improvement, marker="x", color="#0000FF")
    plt.title(f"{algorithm_name}: mejora de la solución contra tiempo")
    plt.xlabel("Tiempo (ms)")
    plt.ylabel("Mejora en %")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def run(**kwargs):
    g, graph = build_graph(**kwargs)

    genetic_algorithm = GeneticAlgorithm(
        g, kwargs["population_size"], kwargs["generations"], kwargs["best_sample_size"], kwargs["mutation_rate"]
    )
    genetic_algorithm.find_optima()
    print(genetic_algorithm.report(total_nodes=len(g)))

    # Por alguna razón, utilizar la misma referencia al grafo ocasiona cambios en los resultados de tiempos
    kwargs["show_graph"] = False
    g, _ = build_graph(**kwargs)
    simulated_annealing = SimulatedAnnealing(
        g, kwargs["initial_temperature"], kwargs["minimum_temperature"], kwargs["cooling_rate"]
    )
    simulated_annealing.find_optima()
    print(simulated_annealing.report(total_nodes=len(g)))

    if not graph:
        return

    multiprocessing.Process(target=graph_genetic, args=(genetic_algorithm.fittest_history,)).start()

    args = (
        [(100 - (v[0] * 100 / v[1])) if i != 0 else 0 for i, v in enumerate(genetic_algorithm.improvement_history)],
        [(t[1] - t[0]) / 10e6 for t in genetic_algorithm.time_history],  # Se hacen postprocesados para evitar alentar
        "Algoritmo genético"                                             # los algoritmos
    )
    multiprocessing.Process(target=graph_costs, args=args).start()

    args = (
        [(100 - (v[0] * 100 / v[1])) if i != 0 else 0 for i, v in enumerate(simulated_annealing.improvement_history)],
        [(t[1] - t[0]) / 10e6 for t in simulated_annealing.time_history],
        "Recocido simulado"
    )
    multiprocessing.Process(target=graph_costs, args=args).start()

    plt.plot(simulated_annealing.bests_history, marker="o", color="#0000FF")
    plt.title("Recocido simulado: mejor distancia por iteración")
    plt.xlabel("Iteración")
    plt.ylabel("Distancia")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
