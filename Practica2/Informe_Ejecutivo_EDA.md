# Informe ejecutivo

## Práctica 2. Análisis Exploratorio de Datos (EDA) y preparación de datasets

**Dataset:** Telco Customer Churn  
**Fuente:** IBM  
**Problema:** Clasificación binaria de cancelación de clientes  
**Herramientas:** Python, pandas, NumPy, Matplotlib, Seaborn, Scikit-learn e imbalanced-learn

## 1. Resumen ejecutivo

El presente trabajo tuvo como objetivo analizar la calidad, distribución y características del dataset _Telco Customer Churn_, así como evaluar diferentes estrategias de preparación de datos y su impacto sobre un modelo de clasificación.

El conjunto de datos contiene 7,043 registros y 21 columnas, con información demográfica, servicios contratados, condiciones comerciales y cargos de clientes de telecomunicaciones.

Durante el análisis se identificaron 11 valores ausentes en `TotalCharges`, un desbalance entre las clases de la variable objetivo `Churn` y diferencias relevantes en las tasas de cancelación según el contrato y los servicios contratados.

Se compararon estrategias de imputación, winsorización y tratamiento del desbalance. Los resultados mostraron que las técnicas de imputación y winsorización produjeron diferencias mínimas en el desempeño predictivo, mientras que el balanceo modificó considerablemente la capacidad del clasificador para identificar cancelaciones.

El modelo final, basado en regresión logística con submuestreo aleatorio, obtuvo un recall del 78.61%, precision del 51.04%, F1-score del 61.89% y Average Precision del 63.05% sobre el conjunto de prueba.

Estos resultados muestran una capacidad relevante para identificar cancelaciones, aunque también evidencian una proporción considerable de falsas alarmas.

## 2. Descripción del dataset

El dataset _Telco Customer Churn_, publicado por IBM, reúne información relacionada con clientes de una empresa de telecomunicaciones.

La unidad de análisis corresponde a un cliente individual y la variable objetivo es `Churn`, que indica si canceló (`Yes`) o permaneció (`No`) con el servicio.

Después de excluir `customerID` y la variable objetivo, se utilizaron 19 características predictoras.

Entre las variables más importantes se encuentran:

- `tenure`: antigüedad del cliente en meses.
    
- `MonthlyCharges`: cargos mensuales.
    
- `TotalCharges`: cargos acumulados.
    
- `Contract`: duración del contrato.
    
- `InternetService`: tipo de servicio de internet.
    

También se incluyen variables demográficas y relacionadas con servicios adicionales.

El conjunto se dividió de manera estratificada en 5,634 registros para entrenamiento y 1,409 para prueba.

## 3. Diagnóstico de calidad de datos

Durante el Data Profiling se identificaron 11 registros con valores vacíos en `TotalCharges`, equivalentes al 0.16% del dataset.

Estos valores inicialmente estaban representados como espacios en blanco, por lo que fue necesario convertir la variable a un tipo numérico para reconocerlos como datos ausentes.

Los 11 registros presentaban `tenure = 0`, lo que permitió plantear una posible relación con clientes que todavía no habían completado su primer periodo de facturación.

No se detectaron registros completamente duplicados ni identificadores de clientes repetidos.

También se analizaron valores inválidos, variables constantes y relaciones entre servicios, sin encontrar inconsistencias en las comprobaciones realizadas.

Respecto a la variable objetivo, se identificó la siguiente distribución:

|Clase|Clientes|Porcentaje|
|---|---|---|
|No cancelaron|5,174|73.46%|
|Sí cancelaron|1,869|26.54%|

La razón de desbalance fue de aproximadamente 2.77, superior al criterio de 1.5 establecido en la práctica.

## 4. Principales hallazgos del análisis exploratorio

El análisis exploratorio permitió identificar diferencias relevantes entre los clientes que cancelaron y aquellos que permanecieron.

### Tipo de contrato

Los contratos mensuales presentaron la mayor tasa de cancelación, con 42.71%, mientras que los contratos de un año registraron 11.27% y los de dos años solamente 2.83%.

Estos resultados sugieren una asociación entre la duración del contrato y la cancelación del servicio.

### Servicio de internet

Los clientes con fibra óptica presentaron una tasa de cancelación del 41.89%, frente al 18.96% de los clientes con DSL y el 7.40% de quienes no tenían servicio de internet.

Las diferencias podrían estar relacionadas con los cargos mensuales, el tipo de contrato u otras características.

### Antigüedad y cargos mensuales

Los diagramas de caja mostraron que los clientes que cancelaron generalmente tenían menor antigüedad.

La mediana visual aproximada fue de 10 meses entre quienes cancelaron y de 38 meses entre quienes permanecieron.

Asimismo, los clientes que cancelaron presentaron cargos mensuales generalmente más elevados, con una mediana visual cercana a 80, frente a aproximadamente 65 entre quienes no cancelaron.

Estos resultados identifican asociaciones, pero no demuestran relaciones causales.

## 5. Comparación de estrategias de preprocesamiento

### 5.1. Imputación de valores ausentes

Se compararon tres estrategias numéricas para `TotalCharges`: media, mediana y una regla de dominio basada en `tenure = 0`.

Los resultados de validación cruzada fueron:

|Estrategia|Recall|F1-score|AP|
|---|---|---|---|
|Media|0.5452|0.5936|0.6612|
|Mediana|0.5452|0.5936|0.6611|
|Regla de dominio|0.5452|0.5934|0.6613|

Las tres alternativas produjeron desempeños prácticamente idénticos.

Se seleccionó la imputación por mediana como referencia por su resistencia a valores extremos y porque no depende de una hipótesis no confirmada sobre los cargos acumulados.

También se realizó un experimento de imputación categórica con 282 ausencias simuladas en `Contract`.

Se comparó la sustitución por moda y por una categoría `Desconocido`, obteniendo diferencias predictivas reducidas.

La incorporación de un indicador binario de ausencia tampoco produjo una mejora relevante.

### 5.2. Tratamiento de valores atípicos

Se compararon dos criterios de winsorización: rango intercuartílico (IQR) y percentiles extremos P5–P95.

El criterio IQR no identificó valores atípicos en las tres variables numéricas analizadas y no modificó ninguna observación.

En contraste, P5–P95 modificó ocho valores de `tenure`, 529 de `MonthlyCharges` y 563 de `TotalCharges`.

La comparación predictiva obtuvo:

|Estrategia|Recall|F1-score|AP|
|---|---|---|---|
|Sin winsorización|0.5452|0.5936|0.6611|
|IQR|0.5452|0.5936|0.6611|
|P5–P95|0.5465|0.5948|0.6613|

Aunque P5–P95 produjo mejoras pequeñas, también modificó observaciones potencialmente válidas. Por ello, se decidió conservar los datos sin winsorización.
### 5.3. Tratamiento del desbalance

Se compararon tres estrategias de remuestreo frente al modelo sin balanceo.

|Estrategia|Precision|Recall|F1-score|AP|
|---|---|---|---|---|
|Sin balanceo|0.6531|0.5452|0.5936|0.6611|
|Sobremuestreo|0.5145|0.8013|0.6265|0.6584|
|Submuestreo|0.5140|0.8027|0.6265|0.6613|
|SMOTENC|0.5449|0.7371|0.6264|0.6396|

Las tres técnicas aumentaron el recall respecto al modelo original, aunque disminuyeron la precision.

El submuestreo obtuvo el recall más alto y la menor variabilidad entre particiones en las métricas de recall, F1-score y AP.

Por esta razón, se seleccionó como estrategia provisional para el clasificador final.
## 6. Evaluación final del clasificador

El modelo seleccionado consistió en una regresión logística con imputación por mediana, codificación categórica, estandarización y submuestreo aleatorio.

El modelo fue entrenado con 5,634 registros y evaluado sobre los 1,409 registros reservados para prueba.

Los resultados fueron:

|Métrica|Validación cruzada|Prueba final|
|---|---|---|
|Accuracy|0.7460|0.7431|
|Precision|0.5140|0.5104|
|Recall|0.8027|0.7861|
|F1-score|0.6265|0.6189|
|Average Precision|0.6613|0.6305|

Los resultados finales fueron ligeramente inferiores a los obtenidos mediante validación cruzada, particularmente en Average Precision.
### Matriz de confusión

La matriz de confusión presentó los siguientes resultados:

|         | Predicción No | Predicción Si |
| ------- | ------------- | ------------- |
| Real No | 753           | 282           |
| Real Si | 80            | 294           |

El modelo logró identificar correctamente 294 de los 374 clientes que realmente cancelaron.

Sin embargo, también clasificó incorrectamente a 282 clientes que permanecieron como posibles cancelaciones.

Esto explica por qué el recall fue relativamente alto, mientras que la precision se mantuvo cercana al 51%.

### Curva Precision-Recall

La curva Precision-Recall obtuvo un Average Precision de 0.6305, superando la referencia correspondiente a la proporción de clientes que cancelaron, aproximadamente 0.2654.

El resultado indica que el modelo permite identificar clientes con mayor concentración de cancelaciones que una selección aleatoria, aunque la precision disminuye cuando se busca recuperar una proporción mayor de casos positivos.

## 7. Decisiones metodológicas

Las principales decisiones adoptadas durante la práctica fueron conservar los registros incompletos, imputar `TotalCharges` mediante la mediana, mantener las variables sin winsorización y seleccionar el submuestreo aleatorio como estrategia de balanceo.

Estas decisiones se fundamentaron tanto en las características de los datos como en los resultados de validación cruzada.

Las técnicas de imputación, estandarización, codificación y remuestreo se integraron en pipelines para que sus parámetros se ajustaran dentro de las particiones de entrenamiento.

El conjunto de prueba se mantuvo reservado hasta la evaluación final, evitando utilizar sus métricas para seleccionar estrategias.

## 8. Conclusiones y limitaciones

La práctica permitió comprobar que las decisiones de preprocesamiento no siempre producen mejoras importantes en el desempeño predictivo.

Las estrategias de imputación y winsorización presentaron diferencias reducidas, mientras que el tratamiento del desbalance produjo cambios considerables en recall y precision.

El clasificador final identificó el 78.61% de las cancelaciones reales, aunque su precision del 51.04% evidencia una cantidad considerable de falsas alarmas.

Entre las principales limitaciones se encuentran la ausencia de información temporal explícita, las ausencias categóricas simuladas y la posibilidad de que algunas variables comerciales estén relacionadas entre sí.

También debe considerarse que el submuestreo elimina parte de los registros mayoritarios durante el entrenamiento y que la evaluación se realizó con un único clasificador de referencia.

En conclusión, los resultados muestran la importancia de evaluar conjuntamente la calidad de los datos, la coherencia de las transformaciones y las métricas de clasificación. La selección de una estrategia debe responder a los objetivos del problema y no depender únicamente de la exactitud general del modelo.

## Uso de inteligencia artificial

Durante el desarrollo de la práctica se utilizó inteligencia artificial como apoyo para organizar las actividades, comprender conceptos estadísticos, estudiar funciones de Python y consultar ejemplos de implementación.

Los experimentos y las métricas reportadas se obtuvieron mediante la ejecución del notebook en Jupyter.