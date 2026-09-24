import subprocess
import logging
import sys
import os


def test_ejecucion_fase2_grafo_pequeno_a():
    # Parámetros de esta prueba específica
    nodos = 500
    destinos = 20  # 1 empresa + resto destinos

    # Ruta del código fase2.py
    nombre_script_principal = "main.py"

    logging.info("\n" + "=" * 60)
    logging.info(f" Ejecutando Test: Subgrafo de {nodos} nodos | {destinos} destinos")
    logging.info("=" * 60)

    comando = [sys.executable, nombre_script_principal, "S2", "-n", str(nodos), "-d", str(destinos)]
    resultado = subprocess.run(comando, capture_output=False, text=True)

    logging.info("\n" + "=" * 60)
    if resultado.returncode == 0:
        logging.info(" Prueba finalizada con éxito")
    else:
        logging.info(" Ocurrió un error durante la prueba")
    logging.info("=" * 60)

    # Aserto necesario para que pytest registre la prueba como exitosa o fallida
    assert resultado.returncode == 0, f"Ocurrió un error en la ejecución (Código: {resultado.returncode})"


def test_ejecucion_fase2_grafo_pequeno_b():
    # Parámetros de esta prueba específica
    nodos = 1500
    destinos = 20  # 1 empresa + resto destinos

    # Ruta del código fase2.py
    nombre_script_principal = "main.py"

    logging.info("\n" + "=" * 60)
    logging.info(f" Ejecutando Test: Subgrafo de {nodos} nodos | {destinos} destinos")
    logging.info("=" * 60)

    comando = [sys.executable, nombre_script_principal, "S2", "-n", str(nodos), "-d", str(destinos)]
    resultado = subprocess.run(comando, capture_output=False, text=True)

    logging.info("\n" + "=" * 60)
    if resultado.returncode == 0:
        logging.info(" Prueba finalizada con éxito")
    else:
        logging.info(" Ocurrió un error durante la prueba")
    logging.info("=" * 60)


def test_ejecucion_fase2_grafo_pequeno_c():
    # Parámetros de esta prueba específica
    nodos = 500
    destinos = 100  # 1 empresa + resto destinos

    # Ruta del código fase2.py
    nombre_script_principal = "main.py"

    logging.info("\n" + "=" * 60)
    logging.info(f" Ejecutando Test: Subgrafo de {nodos} nodos | {destinos} destinos")
    logging.info("=" * 60)

    comando = [sys.executable, nombre_script_principal, "S2", "-n", str(nodos), "-d", str(destinos)]
    resultado = subprocess.run(comando, capture_output=False, text=True)

    logging.info("\n" + "=" * 60)
    if resultado.returncode == 0:
        logging.info(" Prueba finalizada con éxito")
    else:
        logging.info(" Ocurrió un error durante la prueba")
    logging.info("=" * 60)


def test_ejecucion_fase2_grafo_pequeno_d():
    # Parámetros de esta prueba específica
    nodos = 1500
    destinos = 300  # 1 empresa + resto destinos

    # Ruta del código fase2.py
    nombre_script_principal = "main.py"

    logging.info("\n" + "=" * 60)
    logging.info(f" Ejecutando Test: Subgrafo de {nodos} nodos | {destinos} destinos")
    logging.info("=" * 60)

    comando = [sys.executable, nombre_script_principal, "S2", "-n", str(nodos), "-d", str(destinos)]
    resultado = subprocess.run(comando, capture_output=False, text=True)

    logging.info("\n" + "=" * 60)
    if resultado.returncode == 0:
        logging.info(" Prueba finalizada con éxito")
    else:
        logging.info(" Ocurrió un error durante la prueba")
    logging.info("=" * 60)
