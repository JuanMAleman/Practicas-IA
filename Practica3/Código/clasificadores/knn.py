import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin

class KNN(ClassifierMixin, BaseEstimator):
    # Inicializar los parámetros
    def __init__(self, k=5, distancia=2):
        self.k = k
        self.distancia = distancia

    # Guardar los datos de entrenamiento
    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y)
        if self.k < 1 or self.k > len(X):
            raise ValueError("k debe estar entre 1 y el número de registros.")
        if self.distancia not in [1, 2]:
            raise ValueError("La distancia debe ser 1 (Manhattan) o 2 (Euclidiana).")
        self.X_train_ = X
        self.y_train_ = y
        self.classes_ = np.unique(y)
        return self

    # Calcular la distancia entre dos registros
    def calcular_distancia(self, x1, x2):
        diferencia = np.abs(x1 - x2)
        if self.distancia == 1:
            return np.sum(diferencia)
        return np.sqrt(np.sum(diferencia ** 2))

    # Clasificar un registro mediante sus vecinos
    def predecir_uno(self, registro):
        distancias = np.array([
            self.calcular_distancia(registro, muestra)
            for muestra in self.X_train_
        ])
        indices = np.argsort(distancias, kind="stable")[:self.k]
        vecinos = self.y_train_[indices]
        clases, cantidades = np.unique(vecinos, return_counts=True)
        return clases[np.argmax(cantidades)]

    # Clasificar varios registros
    def predict(self, X):
        X = np.asarray(X, dtype=float)
        return np.array([self.predecir_uno(registro) for registro in X])
