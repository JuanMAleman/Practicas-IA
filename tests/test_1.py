import subprocess
import sys
import os

def test_ejecucion_fase2_grafo_pequeno():
    # Parámetros de esta prueba específica
    nodos = 500
    destinos = 20  # 1 empresa + resto destinos

    # Ruta del código fase2.py
    nombre_script_principal = os.path.join("src", "fase2.py")

    print("\n" + "=" * 60)
    print(f" Ejecutando Test: Subgrafo de {nodos} nodos | {destinos} destinos")
    print("=" * 60)

    comando = [sys.executable, nombre_script_principal, str(nodos), str(destinos)]
    resultado = subprocess.run(comando, capture_output=False, text=True)

    print("\n" + "=" * 60)
    if resultado.returncode == 0:
        print(" Prueba finalizada con éxito")
    else:
        print(" Ocurrió un error durante la prueba")
    print("=" * 60)

    # Aserto necesario para que pytest registre la prueba como exitosa o fallida
    assert resultado.returncode == 0, f"Ocurrió un error en la ejecución (Código: {resultado.returncode})"