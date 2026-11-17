from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.naive_bayes import GaussianNB

class NaiveBayes(ClassifierMixin, BaseEstimator):
    # Inicializar los parámetros
    def __init__(self, var_smoothing=1e-9):
        self.var_smoothing = var_smoothing

    # Entrenar el clasificador
    def fit(self, X, y):
        self.modelo_ = GaussianNB(var_smoothing=self.var_smoothing)
        self.modelo_.fit(X, y)
        self.classes_ = self.modelo_.classes_
        return self

    # Realizar predicciones
    def predict(self, X):
        return self.modelo_.predict(X)
