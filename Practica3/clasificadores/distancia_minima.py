import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin

class DistanciaMinima(ClassifierMixin, BaseEstimator):
    # Inicializar el clasificador
    def __init__(self):
        pass

    # Calcular el centroide de cada clase
    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y)
        self.classes_ = np.unique(y)
        self.centroides_ = {}
        for clase in self.classes_:
            self.centroides_[clase] = np.mean(X[y == clase], axis=0)
        return self

    # Calcular la distancia euclidiana
    def calcular_distancia(self, registro, centroide):
        return np.sqrt(np.sum((registro - centroide) ** 2))

    # Clasificar un registro
    def predecir_uno(self, registro):
        distancias = {
            clase: self.calcular_distancia(registro, centroide)
            for clase, centroide in self.centroides_.items()
        }
        return min(distancias, key=distancias.get)

    # Clasificar varios registros
    def predict(self, X):
        X = np.asarray(X, dtype=float)
        return np.array([self.predecir_uno(registro) for registro in X])
