from src.tests import s1_test, s2_test, s3_test
from src import s1, s2, s3
import src.tests as tests
from pathlib import Path
import argparse
import logging
import pytest
import sys

SECTION_OPTIONS = [f"S{i}" for i in range(1, 4)]
SECTIONS = {
    "S1": {"module": s1, "name": "sección 1", "tests": "s1_test.py", "seed": 5},
    "S2": {"module": s2, "name": "sección 2", "tests": "s2_test.py", "seed": 5},
    "S3": {"module": s3, "name": "sección 3", "tests": "s3_test.py", "seed": 14},
}


def valid_distance(value: str) -> float:
    v = float(value)
    if v < 0:
        raise ValueError
    return v


def valid_node_amount_s2(value: str) -> int:
    v = int(value)
    if v < 5:
        raise ValueError
    return v


def valid_node_amount_s3(value: str) -> int:
    v = int(value)
    if v < 4 or v > 15:
        raise ValueError
    return v


if __name__ == "__main__":
    # https://docs.python.org/3.14/library/argparse.html
    parser = argparse.ArgumentParser()
    if "s1" in sys.argv or "S1" in sys.argv:
        parser.add_argument("-a", "--address", help="Dirección del punto del cual se descargará el grafo. "
                                                    "(por defecto = 'Escuela Superior de Cómputo')")
        parser.add_argument("-d", "--distance", type=valid_distance,
                            help="Distancia a la redonda, en metros, que abarcará el grafo. (por defecto = 1000)")
        parser.add_argument("-s", "--start-node", help="Identificador del nodo inicial. "
                                                       "(por defecto = aleatorio)")
        parser.add_argument("-e", "--end-node", help="Identificador del nodo final. "
                                                     "(por defecto = aleatorio)")

    if "s2" in sys.argv or "S2" in sys.argv:
        parser.add_argument("-n", "--nodes", type=valid_node_amount_s2, default=1000,
                            help="Cantidad de nodos para la sección 2. (por defecto 1000)")
        parser.add_argument("-d", "--dst-amount", type=valid_node_amount_s2, default=20,
                            help="Cantidad de destinos para la sección 2. (por defecto 20)")

    if "s3" in sys.argv or "S3" in sys.argv:
        parser.add_argument("-n", "--nodes", type=valid_node_amount_s3, default=10,
                            help="Cantidad de nodos en rango de [4, 15] para la sección 3. (por defecto 10)")
        parser.add_argument("-p", "--population-size", type=lambda v: int(v), default=100,
                            help="Cantidad de poblaciones para algoritmo genético. (por defecto 100)")
        parser.add_argument("-gs", "--generations", type=lambda v: int(v), default=50,
                            help="Cantidad de generaciones para algoritmo genético. (por defecto 50)")
        parser.add_argument("-b", "--best-sample-size", type=lambda v: int(v), default=5,
                            help="Cantidad de individuos a seleccionar como mejores para algoritmo genético. "
                                 "(por defecto 5)")
        parser.add_argument("-m", "--mutation-rate", type=lambda v: float(v), default=0.5,
                            help="Probabilidad de mutación, rango de [0, 1]. (por defecto 0.5)")

        parser.add_argument("-i", "--initial-temperature", type=lambda v: float(v), default=10000,
                            help="Temperatura inicial. (por defecto 10000)")
        parser.add_argument("-mt", "--minimum-temperature", type=lambda v: float(v), default=10,
                            help="Temperatura minima. (por defecto 10)")
        parser.add_argument("-c", "--cooling-rate", type=lambda v: float(v), default=0.8,
                            help="Tasa de enfriamiento. (por defecto 0.8)")

    parser.add_argument("run", type=lambda param: SECTION_OPTIONS[SECTION_OPTIONS.index(param.upper())],
                        help="Sección a ejecutar. Sección 1 (S1): Búsqueda a ciegas; "
                             "Sección 2 (S2): Búsqueda Informada; "
                             "Sección 3 (S3): Búsqueda local")
    parser.add_argument("-t", "--test", choices=["test-only", "both"],
                        help="Opción que indica que las pruebas unitarias se deben ejecutar. "
                             "both: realiza pruebas unitarias y ejecución. "
                             "test-only: solo realiza las pruebas unitarias")
    parser.add_argument("-g", "--show-graph", action="store_true",
                        help="Bandera para mostrar el grafo utilizado en la ejecución/pruebas")

    args = vars(parser.parse_args())
    # logging.basicConfig(level=logging.INFO if args["test"] is None else logging.DEBUG)
    logging.basicConfig(level=logging.INFO)  # Matplot imprime demasiada información

    if args["test"] is not None:
        logging.info("Ejecutando pruebas unitarias...")
        exit_code = pytest.main(["-s", str(Path("src", "tests", SECTIONS[args['run']]['tests']))])

        if args["show_graph"]:
            tests.draw_graph(eval(SECTIONS[args['run']]['tests'].replace(".py", "")).G,
                             SECTIONS[args['run']]["seed"])

        if exit_code != 0:
            logging.fatal("Las pruebas unitarias fallaron. Terminando proceso...")
            sys.exit(exit_code)

        if args["test"] == "test-only":
            logging.info("Todas las pruebas unitarias pasaron.")
            sys.exit(0)

    for section, module_name in SECTIONS.items():
        if args["run"] == section:
            logging.info(f"Ejecutando {module_name['name']}...")
            params = ["show_graph"]

            if args["run"] == "S1":
                params += ["address", "distance", "start_node", "end_node"]

            if args["run"] == "S2":
                params += ["nodes", "dst_amount"]

            if args["run"] == "S3":
                params += ["nodes", "population_size", "generations", "best_sample_size", "mutation_rate"]
                params += ["initial_temperature", "minimum_temperature", "cooling_rate"]

            _args = {k: v for k, v in args.items() if k in params and v is not None and v}

            module_name['module'].run(**_args)
            logging.info(f"Ejecución de la {module_name['name']} terminada")
            sys.exit(0)

    sys.exit(1)
