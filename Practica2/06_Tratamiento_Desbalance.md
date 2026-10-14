# Actividad 6. Tratamiento de desbalance

## 6.1. Objetivo

El objetivo de esta actividad fue analizar el desbalance de clases presente en la variable objetivo `Churn` del dataset _Telco Customer Churn_ y comparar diferentes estrategias para tratarlo.

Se evaluaron tres técnicas de balanceo: sobremuestreo aleatorio, submuestreo aleatorio y SMOTENC, una variante de SMOTE adaptada a conjuntos de datos con variables numéricas y categóricas.

También se utilizó un modelo sin balanceo como referencia para determinar cómo estas estrategias afectan el desempeño de un clasificador de regresión logística.

La comparación se realizó considerando principalmente las métricas precision, recall, F1-score y Average Precision, debido a que la exactitud por sí sola puede resultar insuficiente cuando las clases presentan diferentes cantidades de observaciones.

## 6.2. Diagnóstico del desbalance de clases

Se analizó la distribución de la variable objetivo `Churn` utilizando los 5,634 registros del conjunto de entrenamiento.

Se calcularon las frecuencias absolutas, los porcentajes y la razón de desbalance entre la clase mayoritaria y la minoritaria.

Los resultados obtenidos fueron:

|Clase|Cantidad de registros|Porcentaje|
|---|---|---|
|No|4,139|73.46%|
|Yes|1,495|26.54%|
|**Total**|**5,634**|**100%**|

La razón de desbalance se calculó mediante:

IR = N_mayoritaria / N_minoritaria

Sustituyendo los valores:

IR = 4139 / 1495 = 2.77

De acuerdo con el criterio establecido en la práctica, un conjunto de datos se considera desbalanceado cuando IR es mayor que 1.5.

Como el valor obtenido fue de 2.77, se confirmó que el conjunto de entrenamiento presenta desbalance de clases.

Esto significa que existen aproximadamente 2.77 clientes que no cancelaron su servicio por cada cliente que sí canceló.

Esta diferencia puede afectar el entrenamiento del clasificador, ya que el modelo podría favorecer la clase mayoritaria y presentar dificultades para identificar correctamente a los clientes que cancelan.

Por esta razón, se consideró necesario evaluar diferentes técnicas de tratamiento del desbalance.

## 6.3. Estrategias de balanceo implementadas

Se compararon cuatro escenarios: un modelo sin balanceo y tres estrategias de remuestreo.

### Modelo sin balanceo

Se utilizó la distribución original del conjunto de entrenamiento, sin modificar la cantidad de observaciones de cada clase.

Este modelo permitió establecer un punto de referencia para comparar las técnicas de balanceo.

Su principal limitación es que podría favorecer la clase mayoritaria durante el entrenamiento.

### Sobremuestreo aleatorio

Se implementó `RandomOverSampler` de la biblioteca imbalanced-learn.

Esta técnica aumenta la cantidad de observaciones de la clase minoritaria mediante la selección y repetición aleatoria de registros existentes.

Su principal ventaja es que permite equilibrar las clases sin eliminar observaciones originales.

Sin embargo, la repetición de registros puede favorecer el sobreajuste, por lo que resulta necesario evaluar su desempeño mediante validación cruzada.

### Submuestreo aleatorio

Se utilizó `RandomUnderSampler`, una técnica que reduce la cantidad de registros de la clase mayoritaria mediante una selección aleatoria.

Su objetivo es acercar la cantidad de observaciones de ambas clases, evitando que la clase mayoritaria domine el entrenamiento.

La principal desventaja es que elimina parte de los registros originales durante el ajuste, lo que puede ocasionar pérdida de información relevante.

### SMOTENC

Se utilizó `SMOTENC`, una variante de SMOTE diseñada para datasets que contienen variables numéricas y categóricas.

Esta técnica genera observaciones sintéticas de la clase minoritaria utilizando información de registros cercanos, considerando de forma diferenciada las características categóricas.

Se seleccionó SMOTENC en lugar de SMOTE convencional debido a que el dataset contiene 16 variables categóricas y tres numéricas.

Esto permite evitar la interpolación numérica directa de categorías como `Contract` e `InternetService`.

Sin embargo, los ejemplos sintéticos pueden presentar combinaciones poco representativas de los clientes reales, por lo que su utilidad debe evaluarse experimentalmente.

## 6.4. Diseño experimental

Para comparar las estrategias de balanceo se utilizó un modelo de regresión logística implementado mediante `LogisticRegression` de Scikit-learn.

Se trabajó con el conjunto de entrenamiento compuesto por 5,634 registros y 19 variables predictoras.

La evaluación se realizó mediante validación cruzada estratificada de cinco particiones, utilizando `StratifiedKFold` con una semilla de 42 para favorecer la reproducibilidad.

El preprocesamiento incluyó la imputación por mediana de `TotalCharges`, codificación de variables categóricas mediante `OneHotEncoder` y estandarización utilizando `StandardScaler`.

Para las estrategias de balanceo se utilizó `Pipeline` de imbalanced-learn, integrando las siguientes etapas:

1. Imputación de valores ausentes.
    
2. Aplicación de la técnica de remuestreo.
    
3. Codificación de variables categóricas.
    
4. Estandarización.
    
5. Entrenamiento del clasificador.
    

Las técnicas de remuestreo se aplicaron exclusivamente sobre los registros de entrenamiento de cada partición de validación cruzada.

De esta forma, los datos de validación conservaron su distribución original de clases, evitando fugas de información durante la evaluación.

En el caso de SMOTENC, la imputación se realizó antes del remuestreo y la codificación categórica después, para permitir que el algoritmo reconociera correctamente las variables categóricas.

Se utilizaron las métricas accuracy, precision, recall, F1-score y Average Precision (AP), considerando `Churn = Yes` como la clase positiva.

El conjunto de prueba de 1,409 registros permaneció reservado para la evaluación final del clasificador.

## 6.5. Comparación del desempeño predictivo

Se compararon los resultados promedio obtenidos durante la validación cruzada estratificada de cinco particiones.

|Estrategia|Accuracy|Precision|Recall|F1-score|AP|
|---|---|---|---|---|---|
|Sin balanceo|0.8025|0.6531|0.5452|0.5936|0.6611|
|Sobremuestreo aleatorio|0.7467|0.5145|0.8013|0.6265|0.6584|
|Submuestreo aleatorio|0.7460|0.5140|0.8027|0.6265|0.6613|
|SMOTENC|0.7668|0.5449|0.7371|0.6264|0.6396|

### Interpretación del modelo sin balanceo

El modelo sin balanceo obtuvo un accuracy de 80.25% y una precision de 65.31%, siendo los valores más altos entre las estrategias evaluadas para estas dos métricas.

Sin embargo, su recall fue de 54.52%, lo que indica que identificó aproximadamente el 55% de los clientes que realmente cancelaron el servicio.

Esto significa que una proporción importante de cancelaciones no fue detectada por el clasificador.

Por lo tanto, aunque el accuracy fue relativamente elevado, el modelo presentó limitaciones para identificar a la clase minoritaria.

### Interpretación del sobremuestreo aleatorio

El sobremuestreo aleatorio obtuvo un recall de 80.13%, considerablemente superior al 54.52% del modelo original.

Esto representa una mejora aproximada de 25.61 puntos porcentuales en la identificación de clientes que cancelaron.

El F1-score también aumentó de 0.5936 a 0.6265.

Sin embargo, el accuracy disminuyó a 74.67% y la precision a 51.45%.

Esto indica que el modelo identificó una mayor proporción de cancelaciones reales, pero también generó una proporción mayor de predicciones positivas incorrectas.

### Interpretación del submuestreo aleatorio

El submuestreo aleatorio obtuvo el recall más elevado, con 80.27%.

También alcanzó un F1-score de 0.6265 y un Average Precision de 0.6613.

Estos resultados muestran que el modelo logró identificar una mayor proporción de clientes que cancelaron en comparación con el modelo original.

Sin embargo, su accuracy disminuyó a 74.60% y su precision a 51.40%.

Aunque esta técnica presentó resultados favorables para identificar cancelaciones, debe considerarse que descarta una parte de las observaciones de la clase mayoritaria durante el entrenamiento.

### Interpretación de SMOTENC

SMOTENC obtuvo un recall de 73.71% y una precision de 54.49%.

Estos resultados representan un comportamiento intermedio entre el modelo sin balanceo y las estrategias de remuestreo aleatorio.

Su F1-score fue de 0.6264, muy cercano al obtenido mediante sobremuestreo y submuestreo aleatorio.

Sin embargo, Average Precision disminuyó a 0.6396, siendo el valor más bajo de las cuatro alternativas.

Esto muestra que la generación de registros sintéticos no necesariamente produce mejores resultados en todas las métricas.

### Comparación general

Las tres técnicas de balanceo aumentaron considerablemente el recall respecto al modelo de referencia.

Sin embargo, estas mejoras estuvieron acompañadas de reducciones en accuracy y precision.

Los resultados muestran que el tratamiento del desbalance implica compromisos entre la capacidad para identificar cancelaciones y la cantidad de falsas alarmas generadas.

Por esta razón, no se consideró adecuado seleccionar una estrategia únicamente por su accuracy.

## 6.6. Análisis de estabilidad

Además de comparar los promedios de desempeño, se calculó la desviación estándar de recall, F1-score y Average Precision entre las cinco particiones de validación cruzada.

Los resultados fueron:

|Estrategia|Desv. Recall|Desv. F1-score|Desv. AP|
|---|---|---|---|
|Sin balanceo|0.0420|0.0306|0.0192|
|Sobremuestreo|0.0406|0.0213|0.0215|
|Submuestreo|0.0267|0.0183|0.0189|
|SMOTENC|0.0321|0.0213|0.0237|

La desviación estándar permite observar cuánto variaron las métricas entre las distintas particiones.

El modelo sin balanceo presentó la mayor variabilidad en recall y F1-score.

El sobremuestreo redujo la variabilidad del F1-score respecto al modelo original, aunque la desviación del recall permaneció relativamente elevada.

El submuestreo obtuvo las desviaciones estándar más bajas en las tres métricas analizadas, indicando resultados más uniformes entre las cinco particiones.

Por otra parte, SMOTENC presentó una variabilidad intermedia en recall y F1-score, pero la mayor desviación estándar en Average Precision.

Estos resultados sugieren que el submuestreo mostró un comportamiento más estable dentro del experimento realizado.

Sin embargo, debido a que solamente se utilizaron cinco particiones, no es posible garantizar que esta estabilidad se mantenga con otros conjuntos de datos o divisiones.

## 6.7. Interpretación y decisión metodológica

Los resultados mostraron que el desbalance de clases afecta la forma en que el clasificador identifica a los clientes que cancelaron su servicio.

El modelo sin balanceo obtuvo los mejores resultados de accuracy y precision, pero presentó el recall más bajo.

Por otra parte, el sobremuestreo y el submuestreo aleatorio aumentaron el recall aproximadamente hasta el 80%, mejorando la identificación de la clase minoritaria.

SMOTENC también mejoró el recall, aunque sus resultados fueron inferiores a los del sobremuestreo y submuestreo aleatorio en esta métrica.

El submuestreo obtuvo el recall más alto y la menor variabilidad entre particiones. Sin embargo, su aplicación implica eliminar registros de la clase mayoritaria durante el entrenamiento.

Por ello, se considera que tanto el sobremuestreo como el submuestreo son alternativas relevantes para el problema de clasificación.

Como decisión provisional, se seleccionó el submuestreo aleatorio como candidato para la evaluación final, debido a su recall elevado, F1-score competitivo y menor variabilidad entre particiones.

No obstante, esta selección depende de priorizar la identificación de cancelaciones sobre la reducción de falsas alarmas. La evaluación final deberá considerar también la precision y la matriz de confusión para comprender mejor las consecuencias de los errores de clasificación.

## 6.8. Conclusiones

Durante esta actividad se analizó el desbalance de clases de la variable objetivo `Churn`, identificando una razón de desbalance de 2.77, superior al umbral de 1.5 establecido en la práctica.

Posteriormente, se compararon tres estrategias de tratamiento: sobremuestreo aleatorio, submuestreo aleatorio y SMOTENC, utilizando un modelo sin balanceo como referencia.

Los resultados mostraron que las tres técnicas de balanceo incrementaron el recall del clasificador, especialmente el sobremuestreo y el submuestreo aleatorio, que alcanzaron valores cercanos al 80%.

Sin embargo, este aumento estuvo acompañado de una disminución en accuracy y precision, demostrando que mejorar la identificación de la clase minoritaria puede generar una mayor proporción de falsas alarmas.

El análisis de estabilidad mostró que el submuestreo presentó las menores desviaciones estándar en recall, F1-score y Average Precision.

A partir de estos resultados, se identificó al submuestreo aleatorio como una alternativa prometedora para detectar cancelaciones, aunque no se puede afirmar que sea definitivamente superior a las demás estrategias.

## Uso de inteligencia artificial

Durante el desarrollo de esta actividad se utilizó inteligencia artificial como herramienta de apoyo para organizar las etapas del análisis, comprender los conceptos relacionados con el desbalance de clases y explicar el funcionamiento de las técnicas de sobremuestreo, submuestreo y SMOTENC.

También se consultaron ejemplos de código para configurar los pipelines, aplicar validación cruzada y comparar métricas de evaluación.

Las ejecuciones y los resultados experimentales se obtuvieron mediante Jupyter Notebook. La asistencia de inteligencia artificial se utilizó como apoyo durante el proceso de aprendizaje de la práctica.