from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.svm import SVC

class SVM(ClassifierMixin, BaseEstimator):
    # Inicializar los parámetros
    def __init__(self, kernel="rbf", C=1.0, gamma="scale"):
        self.kernel = kernel
        self.C = C
        self.gamma = gamma

    # Entrenar el clasificador
    def fit(self, X, y):
        self.modelo_ = SVC(kernel=self.kernel, C=self.C, gamma=self.gamma)
        self.modelo_.fit(X, y)
        self.classes_ = self.modelo_.classes_
        return self

    # Realizar predicciones
    def predict(self, X):
        return self.modelo_.predict(X)
