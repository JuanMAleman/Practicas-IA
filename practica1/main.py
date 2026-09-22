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


if __name__ == "__main__":
    # https://docs.python.org/3.14/library/argparse.html
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", help="Dirección del punto del cual se descargará el grafo. "
                                                "(por defecto = 'Escuela Superior de Cómputo')")
    parser.add_argument("-d", "--distance", type=valid_distance,
                        help="Distancia a la redonda, en metros, que abarcará el grafo. (por defecto = 1000)")
    parser.add_argument("-s", "--start-node", help="Identificador del nodo inicial. "
                                                   "(por defecto = aleatorio)")
    parser.add_argument("-e", "--end-node", help="Identificador del nodo final. (por defecto = aleatorio)")
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
    logging.basicConfig(level=logging.INFO if args["test"] is None else logging.DEBUG)

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
            params = ["address", "distance", "show_graph", "start_node", "end_node"]
            _args = {k: v for k, v in args.items() if k in params and v is not None and v}
            module_name['module'].run(**_args)
            logging.info(f"Ejecución de la {module_name['name']} terminada")
            sys.exit(0)

    sys.exit(1)
