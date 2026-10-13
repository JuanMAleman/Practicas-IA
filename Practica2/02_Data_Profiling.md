# Actividad 2. Data Profiling

## 2.1. Inspección inicial

El dataset Telco Customer Churn contiene 7,043 registros y 21 columnas. Durante la inspección estructural se identificaron atributos categóricos y numéricos.

Se observó que `TotalCharges`, a pesar de representar un importe económico, fue interpretada inicialmente como una variable de texto.

## 2.2. Identificación de valores ausentes

El análisis de valores ausentes detectó 11 registros con espacios en blanco en `TotalCharges`, equivalentes aproximadamente al 0.16% del conjunto de datos.

Estos valores no fueron identificados inicialmente como nulos por pandas, debido a que estaban representados mediante cadenas de espacios en blanco.

## 2.3. Análisis de registros afectados

Al examinar los 11 registros, se observaron las siguientes características:

- Todos presentan `tenure = 0`.
    
- Todos contienen un valor registrado en `MonthlyCharges`.
    
- Ninguno registra abandono del servicio (`Churn = No`).
    
- Diez tienen contratos de dos años y uno tiene contrato de un año.
    

### Interpretación

La coincidencia entre la antigüedad de cero meses y la ausencia de cargos acumulados sugiere que estos registros podrían corresponder a clientes recientes cuyo primer ciclo de facturación todavía no se ha completado.

Sin embargo, la información disponible no permite confirmar esta explicación.

Los resultados sugieren que la ausencia de datos podría estar asociada con características observables del cliente, particularmente su antigüedad.

### Decisión preliminar

Se conservarán los registros durante el análisis exploratorio y no se realizará ninguna imputación en esta etapa.

Posteriormente, durante la Actividad 4, se compararán distintas estrategias de imputación numérica para determinar su impacto sobre la distribución de los datos y el desempeño del clasificador.

También se evaluará la conveniencia de crear un indicador binario de ausencia.

## 2.4. Declaración de asistencia de IA

Se utilizó ChatGPT como apoyo para ver ideas sobre el código de identificación de valores ausentes, estructurar la inspección y redactar la interpretación preliminar.

Los 11 registros afectados, sus valores de antigüedad y características contractuales fueron comprobados mediante la ejecución del análisis en Jupyter Notebook.