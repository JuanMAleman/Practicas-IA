from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar el directorio y estilo visual
CARPETA_GRAFICAS = Path("resultados/graficas")
CARPETA_GRAFICAS.mkdir(parents=True, exist_ok=True)
sns.set_theme(style="whitegrid", palette="Set2")

# Guardar la gráfica generada
def guardar_grafica(nombre):
    ruta = CARPETA_GRAFICAS / nombre
    plt.tight_layout()
    plt.savefig(ruta, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Gráfica guardada: {ruta}")

# Comparar clasificadores mediante una métrica
def generar_grafica_comparacion(resultados, metrica, validacion):
    datos = resultados[resultados["validacion"] == validacion].copy()
    if datos.empty:
        return

    datos[metrica] *= 100
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(data=datos, x="clasificador", y=metrica, hue="dataset")
    ax.set_title(f"Comparación de {metrica.upper()} - {validacion}")
    ax.set_xlabel("Clasificador")
    ax.set_ylabel(f"{metrica.upper()} (%)")
    ax.set_ylim(0, 105)
    plt.xticks(rotation=20)
    guardar_grafica(f"{metrica}_{validacion.split()[0].lower()}.png")

# Comparar tiempos de entrenamiento y predicción
def generar_grafica_tiempos(resultados, metrica, validacion):
    datos = resultados[resultados["validacion"] == validacion].copy()
    if datos.empty:
        return

    plt.figure(figsize=(12, 6))
    sns.barplot(data=datos, x="clasificador", y=metrica, hue="dataset")
    plt.title(f"{metrica.replace('_', ' ').title()} - {validacion}")
    plt.xlabel("Clasificador")
    plt.ylabel("Tiempo (segundos)")
    plt.xticks(rotation=20)
    guardar_grafica(f"{metrica}_{validacion.split()[0].lower()}.png")

# Comparar Hold Out y K-Fold por dataset
def generar_grafica_validaciones(resultados, metrica):
    for dataset in resultados["dataset"].unique():
        datos = resultados[resultados["dataset"] == dataset].copy()
        datos[metrica] *= 100
        plt.figure(figsize=(11, 6))
        sns.barplot(data=datos, x="clasificador", y=metrica, hue="validacion")
        plt.title(f"Comparación de validaciones - {dataset}")
        plt.xlabel("Clasificador")
        plt.ylabel(f"{metrica.upper()} (%)")
        plt.ylim(0, 105)
        plt.xticks(rotation=20)
        guardar_grafica(f"validaciones_{dataset.replace(' ', '_')}_{metrica}.png".lower())

# Generar matrices de confusión
def generar_matrices_confusion(resultados):
    for _, fila in resultados.iterrows():
        matriz = fila["matriz_confusion"]
        plt.figure(figsize=(7, 6))
        sns.heatmap(
            matriz, annot=True, fmt="g", cmap="Blues",
            xticklabels=fila["clases"], yticklabels=fila["clases"]
        )
        plt.title(f"{fila['clasificador']} - {fila['dataset']}\n{fila['validacion']}")
        plt.xlabel("Predicción")
        plt.ylabel("Clase real")
        nombre = (
            f"matriz_{fila['dataset']}_{fila['clasificador']}_{fila['validacion']}"
            .lower().replace(" ", "_").replace("/", "_") + ".png"
        )
        guardar_grafica(nombre)

# Comparar modelos originales y optimizados
def generar_graficas_optimizacion(resultados):
    for dataset in resultados["dataset"].unique():
        datos = resultados[resultados["dataset"] == dataset].copy()
        for metrica in ["accuracy", "f1_score"]:
            datos[metrica] *= 100
            plt.figure(figsize=(10, 6))
            sns.barplot(data=datos, x="clasificador", y=metrica, hue="modelo")
            plt.title(f"Original vs Optimizado - {dataset}")
            plt.xlabel("Clasificador")
            plt.ylabel(f"{metrica.upper()} (%)")
            plt.ylim(0, 105)
            guardar_grafica(f"optimizacion_{dataset}_{metrica}.png".lower().replace(" ", "_"))

# Generar todas las gráficas disponibles
def generar_graficas(resultados, resultados_optimizacion=None):
    if resultados is None or resultados.empty:
        print("Primero debes ejecutar la comparación completa.")
        return

    print("\nGENERANDO GRÁFICAS")

    validaciones = ["Hold Out 70/30", "Stratified K-Fold (5)"]
    for validacion in validaciones:
        for metrica in ["accuracy", "f1_score"]:
            generar_grafica_comparacion(resultados, metrica, validacion)
        for metrica in ["tiempo_entrenamiento", "tiempo_prediccion"]:
            generar_grafica_tiempos(resultados, metrica, validacion)

    for metrica in ["accuracy", "f1_score"]:
        generar_grafica_validaciones(resultados, metrica)

    generar_matrices_confusion(resultados)

    if resultados_optimizacion is not None and not resultados_optimizacion.empty:
        generar_graficas_optimizacion(resultados_optimizacion)

    print("\nGráficas generadas correctamente.")
