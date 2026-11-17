import time
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix
)

# Entrenar el modelo y calcular sus métricas
def evaluar_modelo(modelo, X_train, X_test, y_train, y_test):
    inicio = time.perf_counter()
    modelo.fit(X_train, y_train)
    tiempo_entrenamiento = time.perf_counter() - inicio

    inicio = time.perf_counter()
    predicciones = modelo.predict(X_test)
    tiempo_prediccion = time.perf_counter() - inicio

    # Calcular las métricas de clasificación
    return {
        "accuracy": accuracy_score(y_test, predicciones),
        "precision": precision_score(y_test, predicciones, average="macro", zero_division=0),
        "recall": recall_score(y_test, predicciones, average="macro", zero_division=0),
        "f1_score": f1_score(y_test, predicciones, average="macro", zero_division=0),
        "tiempo_entrenamiento": tiempo_entrenamiento,
        "tiempo_prediccion": tiempo_prediccion,
        "matriz_confusion": confusion_matrix(y_test, predicciones, labels=modelo.classes_),
        "clases": np.asarray(modelo.classes_)
    }
