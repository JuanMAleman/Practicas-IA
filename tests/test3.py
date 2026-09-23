import subprocess
import sys
import os

#Parámetros de esta prueba específica
nodos = 500
destinos = 100  # 1 empresa + resto destinos

#Ruta del codigo fase2.py
nombre_script_principal = os.path.join("src", "fase2.py")

print("=" * 60)
print(f" Ejecutando Test: Subgrafo de {nodos} nodos | {destinos} destinos")
print("=" * 60)

#Pasa los parametros a fase2.py
comando = [sys.executable, nombre_script_principal, str(nodos), str(destinos)]
resultado = subprocess.run(comando, capture_output=False, text=True)

print("\n" + "=" * 60)
if resultado.returncode == 0:
    print(" Prueba finalizada con éxito")
else:
    print(" Ocurrió un error durante la prueba")
print("=" * 60)