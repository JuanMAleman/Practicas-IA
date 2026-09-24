from . import format_time
import logging
import time


class Metrics:
    def __init__(self, algorithm: str, timeout: int = 3):
        self._algorithm = algorithm
        self._total_distance = 0
        self._total_edges = 0
        self._path = []

        self._start_time = -1
        self._end_time = -1
        self._timeout = timeout
        self._timer_ended = False

    def _start_timer(self):
        # https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution
        self._start_time = time.time_ns()

    def _end_timer(self):
        self._end_time = time.time_ns()

    @property
    def _is_timeout(self) -> bool:
        if self._start_time == -1:
            logging.warning("_is_timeout: no se realizó llamada a _start_timer")
            return False
        return (time.time_ns() - self._start_time) > self._timeout

    @property
    def _raw_time(self):
        return self._start_time, time.time_ns()

    @property
    def elapsed_time(self) -> str:  # Tiempo de ejecución
        return format_time(self._start_time, self._end_time)

    def reset_metrics(self):
        self._total_distance = 0
        self._total_edges = 0
        self._start_time = -1
        self._end_time = -1
        self._timer_ended = False

    def report(self, total_nodes: int = 0) -> str:
        return (f"Reporte de {self._algorithm}\n"
                f"  Nodos totales:    {total_nodes if total_nodes else 'sin especificar'}\n"
                f"  Ruta:             {' → '.join([str(p) for p in self._path])}\n"
                f"  Distancia total:  {self._total_distance}\n"  # Distancia del nodo inicial al final
                f"  Total de arcos:   {self._total_edges}\n"  # Arcos = saltos del nodo inicial al final
                f"    Tiempo de\n"
                f"    ejecución:      {self.elapsed_time}")
