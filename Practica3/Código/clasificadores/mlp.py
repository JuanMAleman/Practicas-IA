from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.neural_network import MLPClassifier

class MLP(ClassifierMixin, BaseEstimator):
    # Inicializar los parámetros
    def __init__(
        self,
        hidden_layer_sizes=(100,),
        activation="relu",
        solver="adam",
        alpha=0.0001,
        learning_rate_init=0.001,
        max_iter=2000,
        random_state=42
    ):
        self.hidden_layer_sizes = hidden_layer_sizes
        self.activation = activation
        self.solver = solver
        self.alpha = alpha
        self.learning_rate_init = learning_rate_init
        self.max_iter = max_iter
        self.random_state = random_state

    # Entrenar el clasificador
    def fit(self, X, y):
        self.modelo_ = MLPClassifier(
            hidden_layer_sizes=self.hidden_layer_sizes,
            activation=self.activation,
            solver=self.solver,
            alpha=self.alpha,
            learning_rate_init=self.learning_rate_init,
            max_iter=self.max_iter,
            random_state=self.random_state
        )
        self.modelo_.fit(X, y)
        self.classes_ = self.modelo_.classes_
        return self

    # Realizar predicciones
    def predict(self, X):
        return self.modelo_.predict(X)
