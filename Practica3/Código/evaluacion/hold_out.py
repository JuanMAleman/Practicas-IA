import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from clasificadores.distancia_minima import DistanciaMinima
from clasificadores.knn import KNN
from clasificadores.naive_bayes import NaiveBayes
from clasificadores.svm import SVM
from clasificadores.mlp import MLP
from evaluacion.metricas import evaluar_modelo

# Obtener los seis clasificadores
def obtener_clasificadores():
    return {
        "Distancia Minima": DistanciaMinima(),
        "1-NN": KNN(k=1),
        "K-NN": KNN(k=5),
        "Naive Bayes": NaiveBayes(),
        "SVM": SVM(),
        "MLP": MLP()
    }

# Crear un pipeline con normalización
def crear_pipeline(modelo):
    return Pipeline([
        ("escalador", StandardScaler()),
        ("clasificador", clone(modelo))
    ])

# Ejecutar la validación Hold Out 70/30
def ejecutar_hold_out(X, y, nombre_dataset):
    X, y = np.asarray(X), np.asarray(y)
    clases, cantidades = np.unique(y, return_counts=True)
    if len(clases) < 2 or np.min(cantidades) < 2:
        raise ValueError("Cada clase necesita al menos dos registros.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=42, stratify=y
    )

    resultados = []
    print(f"\n{'=' * 65}\nHOLD OUT 70/30 - {nombre_dataset}\n{'=' * 65}")

    # Evaluar todos los clasificadores
    for nombre, modelo_original in obtener_clasificadores().items():
        print(f"\nEvaluando: {nombre}")
        modelo = crear_pipeline(modelo_original)
        metricas = evaluar_modelo(modelo, X_train, X_test, y_train, y_test)
        resultados.append({
            "dataset": nombre_dataset,
            "validacion": "Hold Out 70/30",
            "clasificador": nombre,
            **metricas
        })
        print(f"Accuracy: {metricas['accuracy'] * 100:.2f}%")
        print(f"F1-score: {metricas['f1_score'] * 100:.2f}%")
        print(f"Entrenamiento: {metricas['tiempo_entrenamiento']:.6f} s")
        print(f"Predicción: {metricas['tiempo_prediccion']:.6f} s")

    return pd.DataFrame(resultados)
