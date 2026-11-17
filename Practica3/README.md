# Comparativa de Algoritmos de Clasificación Supervisada

## Descripción del Proyecto

En esta práctica se implementan y comparan los siguientes clasificadores:
1. **Distancia Mínima** 
2. **1-Nearest Neighbor (1-NN)** 
3. **K-Nearest Neighbors (K-NN)** 
4. **Naïve Bayes**
5. **Support Vector Machine (SVM)**
6. **Multi-Layer Perceptron (MLP)**

### Conjuntos de datos evaluados
* **Dataset Iris:** Conjunto de datos clásico utilizado como referencia estándar en problemas de clasificación multiclase.
* **Dataset Sintético:** Conjunto generado artificialmente para analizar el comportamiento de los modelos bajo condiciones controladas y niveles específicos de ruido.

### Metodología de evaluación
* **Validación:** *Hold Out* (70 % entrenamiento / 30 % prueba) y *Stratified K-Fold* (k = 5).
* **Optimización:** Ajuste de hiperparámetros mediante `GridSearchCV` para los modelos K-NN, SVM y MLP.
* **Métricas:** *Accuracy*, *Precision*, *Recall* y *F1-score*

---

## Tecnologías y Herramientas Utilizadas

* **Python 3.15.2:** Lenguaje principal para la lógica de los algoritmos, gestión de experimentos y evaluaciones.
* **NumPy:** Operaciones matemáticas, álgebra lineal y manipulación eficiente de arreglos multidimensionales.
* **Pandas:** Estructuración de los datasets mediante `DataFrame` y cálculo de estadísticas descriptivas.
* **Scikit-learn:** Implementación de modelos (Naïve Bayes, SVM, MLP), preprocesamiento, validación cruzada, métricas y `GridSearchCV`.
* **Matplotlib:** Generación de gráficas base para la visualización de métricas y tiempos.
* **Seaborn:** Estilizado de gráficas estadísticas y generación de matrices de confusión.

---

## Instalación y Ejecución del Proyecto

### 1. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecución del Proyecto 
Una vez configuradas las dependencias, ejecuta el script principal desde la terminal:

```bash
python main.py
```
