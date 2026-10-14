# Actividad 4. Imputación de valores perdidos
## 4.1. Objetivo

El objetivo de esta actividad fue comparar diferentes estrategias para el tratamiento de valores ausentes en variables numéricas y categóricas del dataset _Telco Customer Churn_.

Se analizaron los efectos de estas estrategias sobre la distribución de los datos, la varianza, la aparición de concentraciones artificiales y el desempeño de un clasificador de regresión logística.
## 4.2. Diagnóstico de valores ausentes

Durante el Data Profiling se identificaron 11 registros con valores vacíos en la variable numérica `TotalCharges`, equivalentes aproximadamente al 0.16% de los 7,043 registros del dataset.

Inicialmente, los valores vacíos estaban almacenados como texto, por lo que se utilizó la función `pd.to_numeric()` con el parámetro `errors="coerce"` para convertirlos en valores ausentes reconocidos por pandas (`NaN`).

Se observó que los 11 registros afectados presentaban una antigüedad (`tenure`) igual a cero meses. Por ello, se planteó la hipótesis de que podrían corresponder a clientes que todavía no habían completado su primer ciclo de facturación. Sin embargo, esta explicación no pudo confirmarse únicamente con la información disponible.

No se encontraron valores ausentes originales en las variables categóricas. Por esta razón, posteriormente se realizó un experimento controlado de ausencias simuladas en la variable `Contract`.
## 4.3. Separación de entrenamiento y prueba

El dataset se dividió en dos conjuntos mediante la función `train_test_split()`, utilizando el 80% de los registros para entrenamiento y el 20% para prueba.

|Conjunto|Registros|Valores ausentes en TotalCharges|
|---|---|---|
|Entrenamiento|5,634|8|
|Prueba|1,409|3|
|**Total**|**7,043**|**11**|

Se utilizó una división estratificada mediante `stratify=y` para conservar aproximadamente las proporciones originales de la variable objetivo `Churn`: 73.46% para `No` y 26.54% para `Yes`.

También se excluyeron `customerID`, por ser un identificador, y `Churn`, por ser la variable objetivo, del conjunto de variables predictoras.

Las comparaciones experimentales se realizaron mediante validación cruzada sobre los datos de entrenamiento. El conjunto de prueba se reservó para la evaluación final del clasificador.
## 4.4. Comparación de estrategias de imputación numérica

Se seleccionó la variable `TotalCharges` para comparar tres estrategias de imputación.

**Estrategia A. Imputación por media**

Se utilizó `SimpleImputer(strategy="mean")` para sustituir los valores ausentes mediante el promedio calculado exclusivamente con los datos de entrenamiento.

El valor obtenido fue de 2,302.60.

**Estrategia B. Imputación por mediana**

Se utilizó `SimpleImputer(strategy="median")` para reemplazar los valores ausentes por la mediana de los registros disponibles en entrenamiento.

El valor obtenido fue de 1,398.12.

**Estrategia adicional. Regla de dominio**

Se implementó una transformación personalizada que asigna cero a los valores ausentes de `TotalCharges` cuando `tenure = 0`.

Esta alternativa se fundamentó en la hipótesis de que los clientes afectados todavía no tenían cargos acumulados debido a su antigüedad de cero meses. No obstante, se reconoce que el valor cero no pudo confirmarse como el importe real.

Las tres estrategias permitieron imputar los ocho valores ausentes del conjunto de entrenamiento y los tres del conjunto de prueba, conservando el número de registros y columnas originales.
## 4.5. Impacto sobre la distribución y la varianza

Se compararon las estadísticas descriptivas de `TotalCharges` antes y después de aplicar las estrategias de imputación, utilizando exclusivamente los datos de entrenamiento.

|Estrategia|Media|Mediana|Varianza|Desviación estándar|
|---|---|---|---|---|
|Original|2302.60|1398.12|5194630.36|2279.17|
|Media|2302.60|1401.82|5187252.94|2277.55|
|Mediana|2301.32|1398.12|5188413.13|2277.81|
|Regla de dominio|2299.33|1394.92|5194772.14|2279.20|

Los resultados mostraron que la imputación por media conservó el promedio original, pero produjo una ligera disminución de la varianza.

La imputación por mediana también redujo la varianza y modificó ligeramente el promedio, mientras que la regla de dominio disminuyó la media y produjo un incremento muy pequeño de la varianza.

En general, las tres estrategias provocaron cambios reducidos en las estadísticas globales de `TotalCharges`. Esto podría relacionarse con la baja cantidad de registros incompletos, ya que solamente ocho de los 5,634 registros de entrenamiento presentaban valores ausentes.

Sin embargo, los valores asignados individualmente fueron considerablemente diferentes entre las estrategias.
## 4.6. Concentraciones artificiales

Se analizó si las estrategias de imputación generaban acumulaciones artificiales en los valores utilizados para sustituir los datos ausentes.

|Estrategia|Valor imputado|Frecuencia original|Frecuencia final|
|---|---|---|---|
|Media|2302.60|0|8|
|Mediana|1398.12|0|8|
|Regla de dominio|0|0|8|

Los resultados mostraron que las tres estrategias generaron una concentración artificial de ocho observaciones en el valor correspondiente.

Esto demuestra que los métodos de imputación simple pueden modificar la distribución de frecuencias de una variable, incluso cuando los cambios en su media y varianza globales son pequeños.
## 4.7. Comparación de estrategias de imputación categórica

Debido a que el dataset no presentaba valores ausentes originales en variables categóricas, se seleccionó `Contract` para realizar un experimento controlado.

Se simularon aleatoriamente 282 valores ausentes, equivalentes al 5.01% de los registros de entrenamiento. Se utilizó una semilla fija para garantizar la reproducibilidad del experimento y se conservó intacto el conjunto de prueba.

Se compararon las siguientes estrategias:

**Estrategia A. Imputación por moda**

Se utilizó `SimpleImputer(strategy="most_frequent")`, que identificó `Month-to-month` como la categoría más frecuente.

Los 282 valores ausentes simulados fueron sustituidos por esta categoría.

**Estrategia B. Categoría Desconocido**

Se utilizó `SimpleImputer(strategy="constant", fill_value="Desconocido")`, que sustituyó los valores ausentes mediante una categoría adicional.

Las frecuencias obtenidas fueron:

|Categoría|Moda|Desconocido|
|---|---|---|
|Month-to-month|3,228|2,946|
|Two year|1,294|1,294|
|One year|1,112|1,112|
|Desconocido|0|282|
|**Total**|**5,634**|**5,634**|

La imputación por moda incrementó artificialmente la frecuencia de los contratos mensuales, mientras que la estrategia `Desconocido` permitió conservar la información de que algunos valores se encontraban ausentes sin asignarles una categoría original.
### Recuperación de las categorías simuladas

Como los valores ausentes fueron introducidos de manera artificial, fue posible comparar las imputaciones con las categorías originales.

De los 282 registros seleccionados, 156 correspondían a `Month-to-month`, 65 a `Two year` y 61 a `One year`.

La imputación por moda recuperó correctamente 156 registros, equivalentes al 55.32%, mientras que asignó una categoría diferente de la original a los 126 registros restantes.

La estrategia `Desconocido` no buscó recuperar el contrato original, sino representar explícitamente la ausencia de información.
## 4.8. Diseño experimental del clasificador

Para evaluar el impacto de las estrategias de imputación se utilizó un modelo de regresión logística mediante `LogisticRegression` de Scikit-learn.

Se empleó validación cruzada estratificada de cinco particiones mediante `StratifiedKFold`, utilizando una semilla de 42 para garantizar la reproducibilidad de la división.

Las transformaciones se organizaron mediante `Pipeline` y `ColumnTransformer`, incorporando imputación, codificación categórica mediante `OneHotEncoder` y estandarización con `StandardScaler`.

Los parámetros de preprocesamiento se ajustaron dentro de cada partición de entrenamiento para evitar fugas de información hacia los registros de validación.

Se evaluaron las métricas accuracy, precision, recall, F1-score y Average Precision (AP), considerando `Churn = Yes` como la clase positiva.
## 4.9. Resultados predictivos de imputación numérica

Los resultados promedio obtenidos mediante validación cruzada fueron:

|Estrategia|Accuracy|Precision|Recall|F1-score|AP|
|---|---|---|---|---|---|
|Media|0.8025|0.6531|0.5452|0.5936|0.6612|
|Mediana|0.8025|0.6531|0.5452|0.5936|0.6611|
|Regla de dominio|0.8023|0.6525|0.5452|0.5934|0.6613|

Los resultados indican que las tres estrategias presentaron un desempeño predictivo prácticamente idéntico.

El recall promedio fue de 0.5452 para las tres alternativas, mientras que las diferencias de F1-score y Average Precision fueron mínimas.

Por lo tanto, no existe evidencia suficiente para afirmar que una de las estrategias sea claramente superior.

Se seleccionó la imputación por mediana como alternativa de referencia para las siguientes actividades, debido a su resistencia frente a valores extremos y a que no depende de la hipótesis utilizada por la regla de dominio.
## 4.10. Resultados predictivos de imputación categórica

Para comparar las estrategias categóricas se mantuvo la imputación por mediana en `TotalCharges` y se modificó únicamente el tratamiento de los valores ausentes simulados en `Contract`.

Los resultados obtenidos fueron:

|Estrategia|Accuracy|Precision|Recall|F1-score|AP|
|---|---|---|---|---|---|
|Moda|0.8023|0.6533|0.5438|0.5928|0.6611|
|Desconocido|0.8023|0.6546|0.5405|0.5914|0.6588|

La imputación por moda obtuvo resultados ligeramente superiores en recall, F1-score y Average Precision.

Por otra parte, la categoría `Desconocido` presentó una precision ligeramente mayor.

Las diferencias fueron pequeñas y no permiten concluir que una estrategia sea claramente superior.

Es importante señalar que estos resultados corresponden a un experimento con valores ausentes simulados y no representan problemas de calidad originales de la variable `Contract`.
## 4.11. Indicador binario de ausencia

Debido a que los valores ausentes de `TotalCharges` aparecieron exclusivamente en clientes con `tenure = 0`, se evaluó la incorporación de un indicador binario de ausencia.

Se utilizó `SimpleImputer(add_indicator=True, strategy="median")` para crear una característica adicional que indicara si `TotalCharges` estaba originalmente ausente.

Se comparó el desempeño del clasificador con y sin dicho indicador.

|Métrica|Sin indicador|Con indicador|
|---|---|---|
|Accuracy|0.8025|0.8023|
|Precision|0.6531|0.6528|
|Recall|0.5452|0.5445|
|F1-score|0.5936|0.5931|
|AP|0.6611|0.6615|

Los resultados mostraron que el indicador no produjo una mejora predictiva clara.

Aunque Average Precision aumentó ligeramente, las demás métricas presentaron pequeñas disminuciones.

Esto podría deberse a que la variable `tenure` ya contiene información relacionada con la ausencia de `TotalCharges`, aunque sería necesario realizar un análisis adicional para confirmar esta explicación.

Por lo tanto, se decidió no incluir el indicador binario en el modelo de referencia.
## 4.12. Limitaciones metodológicas

La comparación realizada presenta algunas limitaciones que deben considerarse al interpretar los resultados.

En primer lugar, el número de valores ausentes originales de `TotalCharges` fue reducido, por lo que las diferencias entre las estrategias podrían resultar poco perceptibles en el desempeño general del clasificador.

Además, la regla de dominio se planteó después de examinar los registros incompletos del dataset completo. Por esta razón, se reconoce que la hipótesis fue formulada durante la exploración previa a la evaluación y no debe interpretarse como una regla confirmada de facturación.

Por otra parte, las ausencias categóricas fueron simuladas aleatoriamente y los resultados corresponden a ese patrón específico de ausencia. Las conclusiones podrían cambiar ante otros porcentajes o mecanismos de datos faltantes.

Finalmente, los resultados de desempeño corresponden a validación cruzada sobre el conjunto de entrenamiento. El conjunto de prueba se mantiene reservado para la evaluación final del clasificador.
## 4.13. Conclusiones

Durante esta actividad se compararon distintas estrategias para el tratamiento de valores ausentes en variables numéricas y categóricas.

Las imputaciones por media, mediana y regla de dominio permitieron resolver los valores faltantes de `TotalCharges` sin eliminar registros. Sin embargo, cada estrategia asignó valores diferentes y produjo concentraciones artificiales.

En la comparación categórica, la imputación por moda recuperó correctamente el 55.32% de los contratos ocultados, mientras que la estrategia `Desconocido` permitió representar explícitamente los valores cuya información no estaba disponible.

Los resultados de validación cruzada mostraron diferencias reducidas entre las estrategias de imputación. Asimismo, la incorporación del indicador binario de ausencia no produjo una mejora predictiva relevante.

A partir de estos resultados, se decidió utilizar la imputación por mediana como estrategia de referencia para el tratamiento de `TotalCharges` en las siguientes actividades.
## Uso de inteligencia artificial

Durante el desarrollo de esta actividad se utilizó inteligencia artificial como herramienta de apoyo para organizar las etapas del análisis, comprender conceptos estadísticos y explicar el funcionamiento de algunas funciones de Python.

También se consultaron ejemplos de código para implementar procedimientos de imputación, validación cruzada y evaluación de modelos. Las ejecuciones y los resultados experimentales se obtuvieron en Jupyter Notebook.

La asistencia se utilizó como apoyo durante el proceso de aprendizaje de la práctica.