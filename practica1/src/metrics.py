import time


class Metrics:
    def __init__(self, algorithm: str):
        self._algorithm = algorithm
        self._explored_nodes = 0
        self._total_distance = 0
        self._total_edges = 0
        self._max_elements_in_structure = 0  # Tamaño máximo de la frontera durante la búsqueda

        self._start_time = 0
        self._timer_started = False

    def start_timer(self):
        # https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution
        self._start_time = time.time()
        self._timer_started = True

    @property
    def elapsed_time(self) -> float:  # Tiempo de ejecución
        if not self._timer_started:
            return -1
        self._timer_started = False
        return time.time() - self._start_time

    def report(self) -> str:
        return (f"Reporte de {self._algorithm}\n"
                f"  Nodos expandidos: {self._explored_nodes}\n"
                f"  Distancia total:  {self._total_distance}\n"
                f"  Total de arcos:   {self._total_edges}\n"
                f"    Tamaño de\n"
                f"  frontera máximo:  {self._total_distance}\n"
                f"    Tiempo de\n"
                f"   ejecución (s):   {self.elapsed_time}")
