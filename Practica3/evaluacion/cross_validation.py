import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from evaluacion.hold_out import obtener_clasificadores, crear_pipeline
from evaluacion.metricas import evaluar_modelo

# Ejecutar validación cruzada estratificada
def ejecutar_cross_validation(X, y, nombre_dataset, k=5):
    X, y = np.asarray(X), np.asarray(y)
    clases, cantidades = np.unique(y, return_counts=True)
    if len(clases) < 2 or np.min(cantidades) < k:
        raise ValueError("Cada clase necesita al menos k registros.")

    cv = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
    resultados = []
    columnas = [
        "accuracy", "precision", "recall", "f1_score",
        "tiempo_entrenamiento", "tiempo_prediccion"
    ]

    print(f"\n{'=' * 65}\nSTRATIFIED K-FOLD ({k}) - {nombre_dataset}\n{'=' * 65}")

    # Evaluar cada clasificador en todos los folds
    for nombre, modelo_original in obtener_clasificadores().items():
        metricas_folds = []
        matrices = []
        print(f"\nEvaluando: {nombre}")

        for numero, (train_idx, test_idx) in enumerate(cv.split(X, y), start=1):
            modelo = crear_pipeline(modelo_original)
            metricas = evaluar_modelo(
                modelo, X[train_idx], X[test_idx], y[train_idx], y[test_idx]
            )
            metricas_folds.append(metricas)
            matrices.append(metricas["matriz_confusion"])
            print(f"Fold {numero}: Accuracy = {metricas['accuracy'] * 100:.2f}%")

        # Calcular promedio y desviación estándar
        fila = {
            "dataset": nombre_dataset,
            "validacion": f"Stratified K-Fold ({k})",
            "clasificador": nombre,
            "clases": np.unique(y),
            "matriz_confusion": np.sum(matrices, axis=0)
        }

        for columna in columnas:
            valores = [fold[columna] for fold in metricas_folds]
            fila[columna] = np.mean(valores)
            fila[f"{columna}_std"] = np.std(valores, ddof=1)

        resultados.append(fila)
        print(f"Accuracy promedio: {fila['accuracy'] * 100:.2f}%")
        print(f"Desviación estándar: {fila['accuracy_std'] * 100:.2f}%")

    return pd.DataFrame(resultados)
