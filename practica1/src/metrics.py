import logging
import time
import re


UNITS = {3: "ms", 6: "us", 9: "ns", 12: "ps"}


class Metrics:
    def __init__(self, algorithm: str, timeout: int = 3):
        self._algorithm = algorithm
        self._explored_nodes = 0
        self._total_distance = 0
        self._total_edges = 0
        self._max_elements_in_structure = 0
        self._path = []

        self._start_time = -1
        self._end_time = -1
        self._timeout = timeout
        self._timer_ended = False

    def _start_timer(self):
        # https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution
        self._start_time = time.time()

    def _end_timer(self):
        self._end_time = time.time()

    @property
    def _is_timeout(self) -> bool:
        if self._start_time == -1:
            logging.warning("_is_timeout: no se realizó llamada a _start_timer")
            return False
        return (time.time() - self._start_time) > self._timeout

    @property
    def elapsed_time(self) -> str:  # Tiempo de ejecución
        if self._end_time == -1 or self._start_time == -1:
            logging.warning("_is_timeout: no se realizó llamada a _start_timer o _end_timer")
            return "-1"

        t = self._end_time - self._start_time
        if t > 0.1:
            return f"{t:.4f} s"

        zeros = len(re.findall("^0+", f"{t:.12f}".replace(".", ""))[0])
        while zeros < 13:
            if zeros in UNITS:
                return f"{t * 10 ** zeros:.4f} {UNITS[zeros]}"
            zeros += 1

        logging.warning("_is_timeout: el tiempo de ejecución termino en menos de 1 pico segundo")
        return f"{t:.12f} s"

    def reset_metrics(self):
        self._explored_nodes = 0
        self._total_distance = 0
        self._total_edges = 0
        self._max_elements_in_structure = 0
        self._start_time = -1
        self._end_time = -1
        self._timer_ended = False

    def report(self, start_node: str = "", end_node: str = "", total_nodes: int = 0) -> str:
        return (f"Reporte de {self._algorithm}\n"
                f"  Nodo inicial:     {start_node if start_node else 'sin especificar'}\n"
                f"  Nodo final:       {end_node if end_node else 'sin especificar'}\n"
                f"  Nodos totales:    {total_nodes if total_nodes else 'sin especificar'}\n"
                f"  Ruta:             {' → '.join([str(p) for p in self._path])}\n"
                f"  Nodos expandidos: {self._explored_nodes}\n"
                f"  Distancia total:  {self._total_distance}\n"  # Distancia del nodo inicial al final
                f"  Total de arcos:   {self._total_edges}\n"  # Arcos = saltos del nodo inicial al final
                f"    Tamaño de\n"
                f"  frontera máximo:  {self._max_elements_in_structure}\n"  # Máximos nodos en la estructura de datos
                f"    Tiempo de\n"
                f"    ejecución:      {self.elapsed_time}")
