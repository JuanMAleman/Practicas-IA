Para realizar este análisis se utilizaron las bibliotecas Matplotlib y Seaborn de Python, mediante histogramas, diagramas de caja y gráficas de barras.
## 3.2. Distribuciones numéricas

### Distribución de la antigüedad (`tenure`)
Mediante un histograma se analizó la distribución de la antigüedad de los clientes, expresada en meses.

Se observó una mayor concentración de clientes con antigüedades bajas, principalmente entre 0 y 4 meses. También se identificó un aumento importante en los registros cercanos a los 70 y 72 meses.

En los valores intermedios la frecuencia de clientes es menor, lo cual indica que la distribución no es uniforme y presenta concentraciones en ambos extremos.

Estos resultados son compatibles con el análisis estadístico realizado anteriormente, donde se obtuvo una media de 32.37 meses, una mediana de 29 meses y una asimetría positiva ligera de 0.2395.
### Distribución de los cargos mensuales (`MonthlyCharges`)

El histograma de cargos mensuales permitió observar cómo se distribuyen los importes que pagan los clientes por los servicios contratados.

Se identificó una concentración importante de clientes con cargos bajos, principalmente entre 18 y 23 unidades monetarias. Asimismo, existe otro grupo considerable de clientes con cargos entre aproximadamente 70 y 105.

La distribución presenta varias concentraciones y no es completamente simétrica. Esto concuerda con la asimetría negativa ligera de -0.2205 calculada previamente.

La media de los cargos mensuales fue de 64.76, mientras que la mediana alcanzó 70.35. Estas diferencias podrían estar relacionadas con los distintos servicios y paquetes contratados, aunque sería necesario realizar análisis adicionales para confirmarlo.
## 3.3. Detección visual de valores atípicos

### Diagrama de caja de `tenure`

Se utilizó un diagrama de caja para analizar la dispersión de la antigüedad de los clientes y detectar posibles valores atípicos.

Los resultados mostraron que el primer cuartil corresponde a 9 meses, la mediana a 29 meses y el tercer cuartil a 55 meses. Por lo tanto, el rango intercuartílico fue de 46 meses.

Al aplicar el criterio de 1.5 veces el rango intercuartílico, se obtuvieron límites de -60 y 124 meses.

Debido a que los valores reales se encuentran entre 0 y 72 meses, no se identificaron valores atípicos mediante este criterio.
### Diagrama de caja de `MonthlyCharges`

También se elaboró un diagrama de caja para analizar los cargos mensuales de los clientes.

Se obtuvo un primer cuartil de 35.50, una mediana de 70.35 y un tercer cuartil de 89.85, resultando en un rango intercuartílico de 54.35.

Los límites calculados mediante el criterio de 1.5 veces el rango intercuartílico fueron -46.025 y 171.375.

Como los valores observados se encuentran entre 18.25 y 118.75, tampoco se identificaron valores atípicos mediante este procedimiento.

En ambos casos, los resultados indican que no existe evidencia suficiente para eliminar registros por valores extremos. Sin embargo, posteriormente será necesario evaluar `TotalCharges` y analizar si alguna estrategia de tratamiento de outliers aporta beneficios al modelo de clasificación.
## 3.4. Distribución de la variable objetivo

Se utilizó una gráfica de barras para representar la frecuencia de las categorías de `Churn`, variable que indica si un cliente canceló o no su servicio.

Los resultados mostraron que 5,174 clientes, equivalentes al 73.46%, permanecieron con la compañía, mientras que 1,869 clientes, correspondientes al 26.54%, cancelaron sus servicios.

Esta diferencia muestra un desbalance entre las clases, siendo `No` la categoría mayoritaria y `Yes` la minoritaria.

El desbalance debe considerarse durante el desarrollo del modelo predictivo, ya que un clasificador podría obtener una exactitud aparentemente elevada al favorecer las predicciones de la clase mayoritaria.

Por esta razón, durante la evaluación será necesario considerar métricas como precision, recall, F1-score y PR-AUC, además de comparar estrategias de tratamiento del desbalance.
## 3.5. Relaciones entre variables y cancelación
### Relación entre el tipo de contrato y `Churn`

Se analizó la tasa de cancelación de los clientes según el tipo de contrato mediante tablas de contingencia y una gráfica de barras.

Los clientes con contratos mensuales presentaron una tasa de cancelación del 42.71%, mientras que aquellos con contratos de un año registraron 11.27% y los clientes con contratos de dos años solamente 2.83%.

Estos resultados muestran diferencias importantes entre los tipos de contrato. En particular, los clientes con contratos de menor duración presentan mayores tasas de cancelación.

Por lo tanto, `Contract` podría ser una variable relevante para el modelo predictivo. Sin embargo, estos resultados representan una asociación estadística y no permiten afirmar que la duración del contrato sea la causa directa de la cancelación.
### Relación entre el servicio de internet y `Churn`

Se compararon las tasas de cancelación correspondientes a las categorías de `InternetService`.

Los clientes con servicio de fibra óptica presentaron la tasa de cancelación más elevada, con 41.89%. Por otra parte, los clientes con DSL registraron 18.96%, mientras que aquellos sin servicio de internet presentaron una tasa de 7.40%.

Estos resultados muestran una asociación entre el tipo de servicio de internet y la cancelación.

No obstante, sería necesario considerar otras variables, como los cargos mensuales, el tipo de contrato y la antigüedad, antes de establecer conclusiones más específicas sobre las razones de estas diferencias.
### Relación entre la antigüedad y `Churn`

Para comparar la antigüedad de los clientes que permanecieron y aquellos que cancelaron, se utilizaron diagramas de caja agrupados por la variable objetivo.

Se observó que los clientes que no cancelaron presentan una mediana de antigüedad cercana a 38 meses, mientras que quienes cancelaron tienen una mediana aproximada de 10 meses.

Esto sugiere que los clientes con menor antigüedad presentan una mayor presencia dentro del grupo de cancelaciones.

Adicionalmente, se identificaron algunos posibles valores atípicos cercanos a los 70 y 72 meses dentro del grupo de clientes que cancelaron.

Es importante señalar que estos valores no se consideraron atípicos al analizar el conjunto de datos completo. La diferencia se debe a que cada grupo tiene su propia distribución y rango intercuartílico.

Por lo tanto, estos registros no deben eliminarse únicamente por aparecer como valores extremos en la comparación.
### Relación entre los cargos mensuales y `Churn`

Se utilizó un diagrama de caja para comparar los cargos mensuales entre los clientes que cancelaron y aquellos que permanecieron.

Los clientes que no cancelaron presentaron una mediana aproximada de 65 unidades monetarias, mientras que los clientes que cancelaron mostraron una mediana cercana a 80.

Esto sugiere que los clientes que cancelaron tienden a presentar cargos mensuales superiores.

En ninguno de los dos grupos se observaron valores atípicos según el criterio utilizado por los diagramas de caja.
## 3.6. Hallazgos principales

El análisis exploratorio permitió identificar diferentes características relevantes del dataset.

En primer lugar, se observó que las variables `tenure` y `MonthlyCharges` presentan distribuciones no uniformes y concentraciones de clientes en diferentes intervalos.

Mediante los diagramas de caja no se detectaron valores atípicos globales en estas dos variables utilizando el criterio de 1.5 veces el rango intercuartílico.

También se confirmó visualmente el desbalance de la variable objetivo, donde la mayoría de los clientes no canceló su servicio.

Por otra parte, las comparaciones mostraron que los clientes con contratos mensuales y aquellos que tienen servicio de fibra óptica presentan tasas de cancelación superiores a las de sus respectivos grupos de comparación.

Asimismo, se identificó que los clientes que cancelaron tienden a tener una menor antigüedad y cargos mensuales más elevados que quienes permanecieron.

Estos hallazgos sugieren que las variables `Contract`, `InternetService`, `tenure` y `MonthlyCharges` podrían aportar información relevante para el desarrollo del clasificador.

Finalmente, es importante señalar que las asociaciones identificadas no permiten establecer relaciones causales. Los resultados deberán complementarse con la preparación de los datos y la evaluación de modelos predictivos.
