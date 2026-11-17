import pandas as pd

from datasets.generar_datasets import obtener_datasets, mostrar_informacion_dataset
from evaluacion.hold_out import ejecutar_hold_out
from evaluacion.cross_validation import ejecutar_cross_validation
from evaluacion.optimizacion import ejecutar_optimizacion_completa
from resultados.graficas import generar_graficas

# Mantener resultados durante la ejecución
resultados_comparacion = None
resultados_optimizacion = None

# Mostrar los resultados de la comparación
def mostrar_tabla_comparacion(resultados):
    columnas = [
        "dataset", "validacion", "clasificador",
        "accuracy", "precision", "recall", "f1_score",
        "tiempo_entrenamiento", "tiempo_prediccion"
    ]
    tabla = resultados[columnas].copy()
    for metrica in ["accuracy", "precision", "recall", "f1_score"]:
        tabla[metrica] = (tabla[metrica] * 100).round(2)
    for tiempo in ["tiempo_entrenamiento", "tiempo_prediccion"]:
        tabla[tiempo] = tabla[tiempo].round(6)

    print("\n" + "=" * 120)
    print("TABLA GENERAL DE COMPARACIÓN")
    print("=" * 120)
    print(tabla.to_string(index=False))

# Mostrar las dos tablas de optimización
def mostrar_tablas_optimizacion(resultados):
    metricas = ["accuracy", "precision", "recall", "f1_score"]

    for tipo in ["Original", "Optimizado"]:
        datos = resultados[resultados["modelo"] == tipo].copy()
        for metrica in metricas:
            datos[metrica] = (datos[metrica] * 100).round(2)

        columnas = ["dataset", "clasificador"] + metricas
        print("\n" + "=" * 100)
        print(f"RESULTADOS DE MODELOS {tipo.upper()}")
        print("=" * 100)
        print(datos[columnas].to_string(index=False))

    # Mostrar los parámetros y las mejoras obtenidas
    optimizados = resultados[resultados["modelo"] == "Optimizado"]
    print("\nMEJORES PARÁMETROS Y MEJORAS")
    print("=" * 100)
    for _, fila in optimizados.iterrows():
        print(f"\n{fila['dataset']} - {fila['clasificador']}")
        print(f"Parámetros: {fila['mejores_parametros']}")
        print(f"Mejora Accuracy: {fila['mejora_accuracy']:+.2f} puntos")
        print(f"Mejora F1-score: {fila['mejora_f1']:+.2f} puntos")
        print(f"Resultado: {fila['estado']}")

# Mostrar información de los datasets
def menu_datasets():
    datasets = obtener_datasets()
    while True:
        print("\n========== DATASETS ==========")
        print("[1] Dataset Iris")
        print("[2] Dataset Sintético")
        print("[3] Mostrar ambos")
        print("[0] Regresar")
        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            mostrar_informacion_dataset(datasets["iris"])
        elif opcion == "2":
            mostrar_informacion_dataset(datasets["sintetico"])
        elif opcion == "3":
            for datos in datasets.values():
                mostrar_informacion_dataset(datos)
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")

# Ejecutar Hold Out y K-Fold en ambos datasets
def comparacion_completa():
    global resultados_comparacion
    resultados_totales = []
    print("\nINICIANDO COMPARACIÓN COMPLETA")

    for datos in obtener_datasets().values():
        resultados_totales.append(
            ejecutar_hold_out(datos["X"], datos["y"], datos["nombre"])
        )
        resultados_totales.append(
            ejecutar_cross_validation(datos["X"], datos["y"], datos["nombre"], k=5)
        )

    resultados_comparacion = pd.concat(resultados_totales, ignore_index=True)
    mostrar_tabla_comparacion(resultados_comparacion)
    print("\nComparación completa finalizada.")

# Optimizar automáticamente K-NN, SVM y MLP
def menu_optimizacion():
    global resultados_optimizacion
    print("\nINICIANDO OPTIMIZACIÓN AUTOMÁTICA")
    resultados_optimizacion = ejecutar_optimizacion_completa(obtener_datasets())
    mostrar_tablas_optimizacion(resultados_optimizacion)
    print("\nOptimización finalizada.")

# Generar gráficas de los resultados disponibles
def menu_graficas():
    if resultados_comparacion is None:
        print("\nPrimero debes ejecutar la comparación completa.")
        return

    generar_graficas(resultados_comparacion, resultados_optimizacion)

# Mostrar el menú principal
def mostrar_menu():
    while True:
        print("\n" + "=" * 60)
        print("       COMPARATIVA DE CLASIFICADORES")
        print("=" * 60)
        print("[1] Mostrar información de los datasets")
        print("[2] Ejecutar comparación completa")
        print("[3] Optimizar parámetros")
        print("[4] Generar gráficas")
        print("[0] Salir")
        print("=" * 60)

        opcion = input("\nSelecciona una opción: ").strip()

        try:
            if opcion == "1":
                menu_datasets()
            elif opcion == "2":
                comparacion_completa()
            elif opcion == "3":
                menu_optimizacion()
            elif opcion == "4":
                menu_graficas()
            elif opcion == "0":
                print("\nGracias por utilizar el programa.")
                break
            else:
                print("\nOpción no válida.")
        except KeyboardInterrupt:
            print("\nOperación interrumpida.")
        except Exception as error:
            print(f"\nError durante la ejecución: {error}")

# Iniciar el programa
if __name__ == "__main__":
    mostrar_menu()
