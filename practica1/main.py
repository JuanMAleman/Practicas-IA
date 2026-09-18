from src import s1
import argparse
import logging
import pytest
import sys

SECTIONS = [f"S{i}" for i in range(1, 2)]


def valid_distance(value: str) -> float:
    v = float(value)
    if v < 0:
        raise ValueError
    return v


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", help="Dirección del punto del cual se descargará el grafo.")
    parser.add_argument("-d", "--distance", type=valid_distance,
                        help="Distancia a la redonda, en metros, que abarcará el grafo.")
    parser.add_argument("run", type=lambda param: SECTIONS[SECTIONS.index(param.upper())],
                        help="Sección a ejecutar. Sección 1 (S1): Búsqueda a ciegas; "
                             "Sección 2 (S2): Búsqueda Informada [No implementado]; "
                             "Sección 3 (S3): Búsqueda local [No implementado]")
    parser.add_argument("-t", "--test", choices=["test-only", "both"],
                        help="Opción que indica que las pruebas unitarias se deben ejecutar. "
                             "both: realiza pruebas unitarias y ejecución. "
                             "test-only: solo realiza las pruebas unitarias")

    args = vars(parser.parse_args())

    if args["test"] is not None:
        logging.info("Ejecutando pruebas unitarias...")
        exit_code = pytest.main(["."])
        if exit_code != 0:
            logging.fatal("Las pruebas unitarias fallaron. Terminando proceso...")
            sys.exit(exit_code)

        if args["test"] == "test-only":
            sys.exit(0)

    if args["run"] == "S1":
        logging.info("Ejecutando sección 1...")
        _args = {k: v for k, v in args.items() if k in ["address", "distance"] and v is not None}
        s1.run(**_args)
        logging.info("Ejecución de la sección 1 terminada")
        sys.exit(0)

    sys.exit(1)
