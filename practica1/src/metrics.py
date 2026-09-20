import time
import re


UNITS = {3: "ms", 6: "us", 9: "ns", 12: "ps"}


class Metrics:
    def __init__(self, algorithm: str):
        self._algorithm = algorithm
        self._explored_nodes = 0
        self._total_distance = 0
        self._total_edges = 0
        self._max_elements_in_structure = 0

        self._start_time = 0
        self._timer_started = False

    def start_timer(self):
        # https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution
        self._start_time = time.time()
        self._timer_started = True

    @property
    def elapsed_time(self) -> str:  # Tiempo de ejecución
        if not self._timer_started:
            return "N/A"

        self._timer_started = False

        t = time.time() - self._start_time
        if t > 0.1:
            return f"{t:.4f} s"

        zeros = len(re.findall("^0+", f"{t:.12f}".replace(".", ""))[0])
        while zeros < 13:
            if zeros in UNITS:
                return f"{t * 10 ** zeros:.4f} {UNITS[zeros]}"
            zeros += 1

        return f"{t:.12f} s"

    def reset_metrics(self):
        self._explored_nodes = 0
        self._total_distance = 0
        self._total_edges = 0
        self._max_elements_in_structure = 0
        self._start_time = 0
        self._timer_started = False

    def report(self, start_node: str = "", end_node: str = "", total_nodes: int = 0) -> str:
        return (f"Reporte de {self._algorithm}\n"
                f"  Nodo inicial:     {start_node if start_node else 'sin especificar'}\n"
                f"  Nodo final:       {end_node if end_node else 'sin especificar'}\n"
                f"  Nodos totales:    {total_nodes if total_nodes else 'sin especificar'}\n"
                f"  Nodos expandidos: {self._explored_nodes}\n"
                f"  Distancia total:  {self._total_distance}\n"  # Distancia del nodo inicial al final
                f"  Total de arcos:   {self._total_edges}\n"  # Arcos = saltos del nodo inicial al final
                f"    Tamaño de\n"
                f"  frontera máximo:  {self._max_elements_in_structure}\n"  # Máximos nodos en la estructura de datos
                f"    Tiempo de\n"
                f"    ejecución:      {self.elapsed_time}")
