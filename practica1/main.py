from src.tests import s1_test, s2_test
from pathlib import Path
from src import s1, s2
import argparse
import logging
import pytest
import sys

SECTION_OPTIONS = [f"S{i}" for i in range(1, 3)]
SECTIONS = {
    "S1": {"module": s1, "name": "sección 1", "tests": "s1_test.py"},
    "S2": {"module": s2, "name": "sección 2", "tests": "s2_test.py"},
}


def valid_distance(value: str) -> float:
    v = float(value)
    if v < 0:
        raise ValueError
    return v


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # https://docs.python.org/3.14/library/argparse.html
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", help="Dirección del punto del cual se descargará el grafo.")
    parser.add_argument("-d", "--distance", type=valid_distance,
                        help="Distancia a la redonda, en metros, que abarcará el grafo.")
    parser.add_argument("run", type=lambda param: SECTION_OPTIONS[SECTION_OPTIONS.index(param.upper())],
                        help="Sección a ejecutar. Sección 1 (S1): Búsqueda a ciegas; "
                             "Sección 2 (S2): Búsqueda Informada; "
                             "Sección 3 (S3): Búsqueda local [No implementado]")
    parser.add_argument("-t", "--test", choices=["test-only", "both"],
                        help="Opción que indica que las pruebas unitarias se deben ejecutar. "
                             "both: realiza pruebas unitarias y ejecución. "
                             "test-only: solo realiza las pruebas unitarias")
    parser.add_argument("-dr", "--draw", action="store_true",
                        help="Bandera para mostrar el grafo utilizado en la ejecución/pruebas")

    args = vars(parser.parse_args())

    if args["test"] is not None:
        logging.info("Ejecutando pruebas unitarias...")
        exit_code = pytest.main([str(Path("src", "tests", SECTIONS[args['run']]['tests']))])

        if args["draw"]:
            eval(SECTIONS[args['run']]['tests'].replace(".py", "")).draw_graph()
        if exit_code != 0:
            logging.fatal("Las pruebas unitarias fallaron. Terminando proceso...")
            sys.exit(exit_code)

        if args["test"] == "test-only":
            sys.exit(0)

    for section, module_name in SECTIONS.items():
        if args["run"] == section:
            logging.info(f"Ejecutando {module_name['name']}...")
            _args = {k: v for k, v in args.items() if k in ["address", "distance", "draw"] and v is not None}
            module_name['module'].run(**_args)
            logging.info(f"Ejecución de la {module_name['name']} terminada")
            sys.exit(0)

    sys.exit(1)
