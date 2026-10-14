# Actividad 5. Detección y tratamiento de outliers

## 5.1. Objetivo

El objetivo de esta actividad fue identificar posibles valores atípicos en las variables numéricas del dataset _Telco Customer Churn_ y comparar dos estrategias de winsorización: una basada en el rango intercuartílico (IQR) y otra mediante percentiles extremos P5–P95.

Se buscó analizar los efectos de ambas estrategias sobre la distribución de los datos, las estadísticas descriptivas y el desempeño de un modelo de regresión logística, con la finalidad de determinar si el tratamiento de valores extremos aporta beneficios al proceso de clasificación.

## 5.2. Detección de valores atípicos mediante IQR

Se seleccionaron las variables numéricas `tenure`, `MonthlyCharges` y `TotalCharges` para identificar posibles valores atípicos mediante el criterio de 1.5 veces el rango intercuartílico.

Los cálculos se realizaron sobre los 5,634 registros de entrenamiento para evitar utilizar información del conjunto de prueba.

Se obtuvieron los siguientes resultados:

|Variable|Q1|Q3|IQR|Límite inferior|Límite superior|
|---|---|---|---|---|---|
|tenure|9.00|55.00|46.00|-60.00|124.00|
|MonthlyCharges|35.66|90.00|54.34|-45.84|171.51|
|TotalCharges|407.28|3838.61|3431.34|-4739.73|8985.62|

Para calcular los límites se utilizaron las expresiones:

- Límite inferior = Q1 − 1.5 × IQR
    
- Límite superior = Q3 + 1.5 × IQR
    

Posteriormente, se contabilizaron los registros que superaban los límites establecidos.

|Variable|Valores atípicos detectados|Porcentaje|
|---|---|---|
|tenure|0|0.00%|
|MonthlyCharges|0|0.00%|
|TotalCharges|0|0.00%|

Los resultados mostraron que ninguna de las tres variables presentaba valores fuera de los límites definidos por el criterio IQR.

Esto significa que no se identificaron valores atípicos mediante esta regla estadística. Sin embargo, no implica que todos los datos estén libres de errores ni que no existan valores extremos bajo otros criterios.

## 5.3. Winsorización por IQR

Se aplicó winsorización utilizando los límites inferior y superior obtenidos mediante el criterio de 1.5 × IQR.

La winsorización consiste en sustituir los valores que se encuentran fuera de determinados límites por el valor del límite correspondiente, sin eliminar registros.

Para aplicar el tratamiento se utilizó la función `clip()` de pandas sobre una copia independiente del conjunto de entrenamiento.

Los resultados obtenidos fueron:

|Variable|Valores modificados|
|---|---|
|tenure|0|
|MonthlyCharges|0|
|TotalCharges|0|

La aplicación de winsorización por IQR no modificó ninguna observación, ya que todos los valores originales estaban dentro de los límites calculados.

Además, se conservaron los 5,634 registros y las 19 variables predictoras. Los ocho valores ausentes de `TotalCharges` también permanecieron sin modificaciones.

Por lo tanto, esta estrategia no produjo cambios en las distribuciones originales durante el análisis descriptivo.

## 5.4. Winsorización por percentiles P5–P95

Como segunda estrategia, se aplicó winsorización mediante percentiles extremos.

Se utilizaron los percentiles 5 y 95, calculados exclusivamente con los datos de entrenamiento.

Los límites obtenidos fueron:

|Variable|Percentil 5|Percentil 95|
|---|---|---|
|tenure|1.00|72.00|
|MonthlyCharges|19.65|107.37|
|TotalCharges|49.65|6979.83|

Los valores inferiores al percentil 5 fueron sustituidos por el límite inferior, mientras que aquellos superiores al percentil 95 fueron limitados al valor correspondiente.

Después de aplicar esta estrategia se obtuvieron los siguientes resultados:

|Variable|Valores modificados|
|---|---|
|tenure|8|
|MonthlyCharges|529|
|TotalCharges|563|

A diferencia de la winsorización por IQR, el tratamiento P5–P95 modificó numerosas observaciones, principalmente en `MonthlyCharges` y `TotalCharges`.

En `tenure`, los ocho registros modificados correspondían a clientes con una antigüedad de cero meses, cuyos valores fueron sustituidos por un mes.

Este resultado es importante porque una antigüedad de cero meses puede representar información válida sobre clientes recién incorporados. Por lo tanto, su modificación podría afectar el significado de los datos.

En `MonthlyCharges`, los valores se limitaron al intervalo de 19.65 a 107.37, mientras que en `TotalCharges` se restringieron al intervalo de 49.65 a 6979.83.

La aplicación de este tratamiento conservó las dimensiones originales del conjunto de entrenamiento y mantuvo los ocho valores ausentes de `TotalCharges`, ya que la winsorización no sustituye valores nulos.

## 5.5. Comparación de estadísticas descriptivas

Para determinar el impacto de ambas estrategias se compararon la media, mediana, desviación estándar, mínimo y máximo de cada variable antes y después de la winsorización.

|Estrategia|Variable|Media|Mediana|Desv. estándar|Mínimo|Máximo|
|---|---|---|---|---|---|---|
|Original|tenure|32.49|29.00|24.57|0.00|72.00|
|Original|MonthlyCharges|64.93|70.50|30.14|18.40|118.75|
|Original|TotalCharges|2302.60|1398.12|2279.17|18.85|8684.80|
|IQR|tenure|32.49|29.00|24.57|0.00|72.00|
|IQR|MonthlyCharges|64.93|70.50|30.14|18.40|118.75|
|IQR|TotalCharges|2302.60|1398.12|2279.17|18.85|8684.80|
|P5–P95|tenure|32.49|29.00|24.57|1.00|72.00|
|P5–P95|MonthlyCharges|64.73|70.50|29.79|19.65|107.37|
|P5–P95|TotalCharges|2270.60|1398.12|2202.13|49.65|6979.83|

### Interpretación de los resultados

La winsorización por IQR no produjo modificaciones en las estadísticas descriptivas, debido a que no se detectaron valores fuera de sus límites.

Por otra parte, P5–P95 sí generó cambios, especialmente en los valores mínimos y máximos.

En `tenure`, el valor mínimo pasó de cero a un mes, mientras que la media y la desviación estándar permanecieron prácticamente iguales al redondear a dos decimales.

En `MonthlyCharges`, la media disminuyó de 64.93 a 64.73 y la desviación estándar pasó de 30.14 a 29.79. Esto indica una reducción ligera de la dispersión.

En `TotalCharges` se observó el mayor cambio. La media disminuyó de 2302.60 a 2270.60 y la desviación estándar pasó de 2279.17 a 2202.13.

La mediana de las tres variables permaneció sin cambios, lo que indica que el tratamiento afectó principalmente los extremos de sus distribuciones.

En general, la winsorización P5–P95 redujo la dispersión de los cargos mensuales y acumulados. Sin embargo, una menor dispersión no implica necesariamente una mayor calidad de los datos o una mejora del modelo predictivo.

## 5.6. Comparación visual mediante histogramas y boxplots

Se generaron histogramas y diagramas de caja para comparar las distribuciones originales con las obtenidas mediante winsorización por IQR y P5–P95.

### Análisis visual de TotalCharges

El histograma original mostró una distribución con asimetría positiva, caracterizada por una concentración elevada de clientes con cargos acumulados bajos y una cola extendida hacia valores superiores.

Después de aplicar winsorización por IQR, la distribución permaneció sin cambios.

En cambio, la winsorización P5–P95 limitó los cargos acumulados superiores a 6979.83, produciendo una concentración de observaciones cerca de ese límite.

Los diagramas de caja confirmaron que el valor máximo disminuyó de 8684.80 a 6979.83, mientras que la mediana permaneció en 1398.12.

Estos resultados muestran que P5–P95 modificó los extremos de la distribución sin alterar su tendencia central.

### Análisis de MonthlyCharges

En la distribución original se identificaron concentraciones de clientes con cargos mensuales bajos y otros grupos con importes intermedios y elevados.

El histograma y el diagrama de caja correspondientes a IQR permanecieron iguales a los originales.

Después de aplicar P5–P95, se observó una acumulación de valores cerca del límite superior de 107.37.

La desviación estándar disminuyó ligeramente, aunque la mediana y la estructura central de la distribución permanecieron prácticamente iguales.

Esto indica que el tratamiento redujo el rango de los cargos mensuales, pero también modificó observaciones que no habían sido identificadas como valores atípicos mediante IQR.

### Análisis de tenure

La distribución original de `tenure` mostró concentraciones importantes de clientes con poca antigüedad y de clientes cercanos a los 72 meses.

La winsorización por IQR no produjo modificaciones.

Por otra parte, P5–P95 sustituyó ocho valores de cero meses por un mes.

Las diferencias visuales fueron mínimas, ya que solamente se modificó una pequeña proporción de los registros y los valores permanecieron dentro del mismo intervalo del histograma.

Los diagramas de caja también resultaron prácticamente iguales, con excepción del valor mínimo.

Sin embargo, este cambio es relevante desde el punto de vista del dominio, debido a que una antigüedad igual a cero puede representar a clientes nuevos y no necesariamente un error.

## 5.7. Evaluación del desempeño del clasificador

Para comparar el impacto de la winsorización sobre el desempeño predictivo, se utilizó un modelo de regresión logística y validación cruzada estratificada de cinco particiones.

Se evaluaron tres estrategias:

- Sin winsorización.
    
- Winsorización mediante IQR.
    
- Winsorización mediante percentiles P5–P95.
    

Se mantuvieron constantes la imputación por mediana, la codificación categórica mediante `OneHotEncoder`, la estandarización con `StandardScaler` y la configuración del clasificador.

Las transformaciones se integraron mediante pipelines para calcular los límites de winsorización dentro de cada partición de entrenamiento y evitar fugas de información.

Los resultados promedio fueron:

|Estrategia|Accuracy|Precision|Recall|F1-score|AP|
|---|---|---|---|---|---|
|Sin winsorización|0.8025|0.6531|0.5452|0.5936|0.6611|
|IQR|0.8025|0.6531|0.5452|0.5936|0.6611|
|P5–P95|0.8030|0.6541|0.5465|0.5948|0.6613|

### Interpretación del desempeño

El modelo sin winsorización obtuvo un accuracy de 80.25%, un recall de 54.52% y un F1-score de 59.36%.

La winsorización mediante IQR produjo los mismos resultados promedio redondeados, lo que es coherente con la ausencia de modificaciones en el análisis descriptivo.

La estrategia P5–P95 presentó resultados ligeramente superiores en todas las métricas.

El accuracy aumentó de 80.25% a 80.30%, mientras que el recall pasó de 54.52% a 54.65%. Asimismo, el F1-score aumentó de 59.36% a 59.48%.

Sin embargo, estas diferencias fueron muy pequeñas y no permiten afirmar que la winsorización por percentiles genere una mejora predictiva consistente.

Además, el tratamiento P5–P95 modificó numerosas observaciones potencialmente válidas, por lo que sus beneficios deben considerarse junto con los cambios realizados en los datos.

## 5.8. Interpretación y decisión metodológica

Los experimentos mostraron que las dos estrategias de winsorización presentan comportamientos diferentes.

La winsorización por IQR no identificó valores atípicos ni modificó observaciones en las tres variables analizadas.

Por otra parte, P5–P95 modificó los extremos de las distribuciones, disminuyó la dispersión de algunas variables y produjo pequeñas mejoras en el desempeño del clasificador.

Sin embargo, dichas mejoras fueron mínimas y no representan evidencia suficiente para concluir que la transformación sea claramente superior.

Además, la winsorización por percentiles modificó valores potencialmente válidos, como los registros con `tenure = 0`.

Por lo tanto, se decidió mantener las variables sin winsorización como estrategia de referencia para los siguientes experimentos.

Esta decisión busca conservar la información original y evitar modificaciones que no hayan demostrado beneficios predictivos relevantes.

La evaluación final del clasificador sobre los datos de prueba se realizará posteriormente, una vez completadas las demás estrategias de preparación de datos.

## 5.9. Conclusiones

Durante esta actividad se identificaron y analizaron posibles valores atípicos en las variables numéricas del dataset _Telco Customer Churn_, utilizando el criterio IQR y la winsorización mediante percentiles extremos.

El análisis mediante IQR no identificó valores fuera de los límites establecidos, por lo que la aplicación de esta estrategia no produjo cambios en los datos.

En contraste, la winsorización P5–P95 modificó ocho valores de `tenure`, 529 de `MonthlyCharges` y 563 de `TotalCharges`, reduciendo los rangos de las variables y la dispersión de los cargos mensuales y acumulados.

Las comparaciones visuales permitieron observar que la winsorización por percentiles produjo concentraciones en los límites establecidos, especialmente en los cargos acumulados.

Finalmente, los resultados de validación cruzada mostraron que P5–P95 obtuvo mejoras predictivas muy pequeñas respecto al modelo sin winsorización.

Debido a que estas diferencias fueron reducidas y el tratamiento modificó observaciones potencialmente válidas, se decidió conservar los datos sin winsorización en el modelo de referencia.
## Uso de inteligencia artificial

Durante el desarrollo de esta actividad se utilizó inteligencia artificial como herramienta de apoyo para organizar las etapas del análisis, comprender los conceptos de detección de valores atípicos y winsorización, así como explicar el funcionamiento de diferentes funciones de Python.

También se consultaron ejemplos de código para implementar procedimientos estadísticos, generar visualizaciones e integrar las transformaciones dentro de pipelines de validación cruzada.

Las ejecuciones y los resultados experimentales se obtuvieron en Jupyter Notebook. La asistencia de inteligencia artificial se utilizó como apoyo durante el proceso de aprendizaje de la práctica.