import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold

from clasificadores.knn import KNN
from clasificadores.svm import SVM
from clasificadores.mlp import MLP
from evaluacion.hold_out import crear_pipeline
from evaluacion.metricas import evaluar_modelo

# Definir los parámetros que se probarán
def obtener_configuraciones():
    return {
        "K-NN": {
            "modelo": KNN(),
            "parametros": {
                "clasificador__k": [1, 3, 5, 7, 9],
                "clasificador__distancia": [1, 2]
            }
        },
        "SVM": {
            "modelo": SVM(),
            "parametros": [
                {
                    "clasificador__kernel": ["linear"],
                    "clasificador__C": [0.1, 1, 10, 100]
                },
                {
                    "clasificador__kernel": ["rbf"],
                    "clasificador__C": [0.1, 1, 10, 100],
                    "clasificador__gamma": ["scale", "auto", 0.01, 0.1, 1]
                }
            ]
        },
        "MLP": {
            "modelo": MLP(),
            "parametros": {
                "clasificador__hidden_layer_sizes": [(50,), (100,), (100, 50)],
                "clasificador__activation": ["relu", "tanh"],
                "clasificador__alpha": [0.0001, 0.001, 0.01],
                "clasificador__learning_rate_init": [0.001, 0.01]
            }
        }
    }

# Ejecutar la optimización de un dataset
def optimizar_modelo(X, y, nombre_dataset, k=5):
    X, y = np.asarray(X), np.asarray(y)
    _, cantidades = np.unique(y, return_counts=True)
    if len(cantidades) < 2 or np.min(cantidades) < k:
        raise ValueError("No existen suficientes registros para optimizar.")

    # Reservar el conjunto de prueba antes de buscar parámetros
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=42, stratify=y
    )
    cv = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
    resultados = []

    print(f"\n{'=' * 75}\nOPTIMIZACIÓN - {nombre_dataset}\n{'=' * 75}")

    for nombre, configuracion in obtener_configuraciones().items():
        print(f"\nOptimizando: {nombre}")
        modelo_original = configuracion["modelo"]

        # Evaluar la configuración inicial
        metricas_original = evaluar_modelo(
            crear_pipeline(modelo_original), X_train, X_test, y_train, y_test
        )

        # Buscar los mejores parámetros mediante validación cruzada
        busqueda = GridSearchCV(
            estimator=crear_pipeline(modelo_original),
            param_grid=configuracion["parametros"],
            scoring="f1_macro",
            cv=cv,
            n_jobs=-1,
            refit=True
        )
        busqueda.fit(X_train, y_train)

        # Evaluar el modelo optimizado en el mismo conjunto de prueba
        metricas_optimizadas = evaluar_modelo(
            busqueda.best_estimator_, X_train, X_test, y_train, y_test
        )

        mejora_accuracy = (
            metricas_optimizadas["accuracy"] - metricas_original["accuracy"]
        ) * 100
        mejora_f1 = (
            metricas_optimizadas["f1_score"] - metricas_original["f1_score"]
        ) * 100

        estado = (
            "Mejoró" if mejora_f1 > 0 else
            "Empeoró" if mejora_f1 < 0 else "Sin cambios"
        )

        mejores_parametros = {
            clave.replace("clasificador__", ""): valor
            for clave, valor in busqueda.best_params_.items()
        }

        print(f"Mejores parámetros: {mejores_parametros}")
        print(f"F1-score CV: {busqueda.best_score_ * 100:.2f}%")
        print(f"F1 original: {metricas_original['f1_score'] * 100:.2f}%")
        print(f"F1 optimizado: {metricas_optimizadas['f1_score'] * 100:.2f}%")
        print(f"Mejora F1: {mejora_f1:+.2f} puntos porcentuales")
        print(f"Resultado: {estado}")

        # Guardar los resultados en memoria
        for tipo, metricas in [
            ("Original", metricas_original),
            ("Optimizado", metricas_optimizadas)
        ]:
            resultados.append({
                "dataset": nombre_dataset,
                "clasificador": nombre,
                "modelo": tipo,
                **{
                    clave: valor for clave, valor in metricas.items()
                    if clave not in ["matriz_confusion", "clases"]
                },
                "mejora_accuracy": mejora_accuracy if tipo == "Optimizado" else 0,
                "mejora_f1": mejora_f1 if tipo == "Optimizado" else 0,
                "estado": estado if tipo == "Optimizado" else "Modelo base",
                "mejores_parametros": (
                    str(mejores_parametros) if tipo == "Optimizado"
                    else "Parámetros iniciales"
                )
            })

    return pd.DataFrame(resultados)

# Optimizar ambos datasets en orden
def ejecutar_optimizacion_completa(datasets):
    resultados = [
        optimizar_modelo(datos["X"], datos["y"], datos["nombre"])
        for datos in datasets.values()
    ]
    return pd.concat(resultados, ignore_index=True)
