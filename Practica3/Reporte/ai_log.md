# Bitácora de uso de inteligencia artificial generativa

## 1. Información general

* **Proyecto:** Comparativa de clasificadores mediante Python.

* **Herramienta utilizada:** ChatGPT (OpenAI).
* **Modelo:** GPT-6.
* **Uso específico:** Análisis de complejidad temporal e interpretación de los resultados experimentales.

* **Herramienta utilizada:** Gemini (Google).
* **Modelo:** Gemini 4 Hydrogen.
* **Uso específico:** Formateo de documentación en lenguaje Markdown y estructuración del archivo `README.md`.

### Objetivo de la utilización de IA

La inteligencia artificial generativa se utilizó como herramienta de apoyo para revisar, analizar y documentar el proyecto de clasificación desarrollado en Python.

Su utilización tuvo como finalidad facilitar la comprensión de algunos conceptos de aprendizaje automático, verificar la consistencia de los resultados experimentales, revisar el análisis de complejidad temporal y mejorar la documentación del proyecto.

---

## 2. Actividades realizadas con asistencia de IA

### 2.1 Análisis de complejidad temporal

Se solicitó asistencia para estudiar la complejidad temporal de los seis clasificadores utilizados:

* Distancia Mínima.
* 1-NN.
* K-NN.
* Naïve Bayes.
* SVM.
* Perceptrón Multicapa (MLP).

Se analizaron las operaciones realizadas durante el entrenamiento y la predicción, considerando la cantidad de registros, características, clases, vecinos, vectores de soporte y neuronas de las redes. También se revisó la complejidad de almacenamiento para complementar el análisis.

### 2.2 Revisión de resultados experimentales

* Se compartieron los resultados obtenidos mediante *Hold Out* 70/30 y *Stratified K-Fold* con cinco particiones.
* La herramienta proporcionó asistencia para interpretar las métricas *Accuracy*, *Precision*, *Recall* y *F1-score*, así como los tiempos de entrenamiento y predicción.
* También se utilizó para comparar el comportamiento de los clasificadores en los datasets *Iris* y *Sintético*.

### 2.3 Análisis de optimización de hiperparámetros

* Se proporcionaron los resultados obtenidos mediante `GridSearchCV` para los clasificadores K-NN, SVM y MLP.
* Se solicitó interpretar las configuraciones seleccionadas, identificar las mejoras o disminuciones de rendimiento y explicar por qué una configuración seleccionada mediante validación cruzada no necesariamente obtiene mejores resultados en el conjunto de prueba.

---

## 3. Ejemplos de solicitudes realizadas

A continuación se presentan ejemplos representativos de las instrucciones proporcionadas a la herramienta:

#### Solicitud 1: Complejidad temporal
> "Realiza un análisis de complejidad temporal de los seis clasificadores, diferenciando las etapas de entrenamiento y predicción. Verifica las expresiones considerando las implementaciones que estoy utilizando."

#### Solicitud 2: Interpretación de resultados
> "Analiza los resultados de Hold Out y K-Fold para los datasets Iris y Sintético. Ayúdame a explicar las diferencias entre clasificadores y las métricas obtenidas."

#### Solicitud 3: Optimización
> "Revisa los resultados de GridSearchCV para K-NN, SVM y MLP y explica si las configuraciones optimizadas consiguieron mejorar el rendimiento respecto a las configuraciones iniciales."

#### Solicitud 4: README
> "Prepara un archivo README.md que explique las tecnologías utilizadas y las instrucciones de instalación y ejecución del proyecto."
