# Actividad 2. Data Profiling

## 2.1. Inspección inicial

El dataset Telco Customer Churn contiene 7,043 registros y 21 columnas.

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

Los resultados sugieren que la ausencia de datos podría estar asociada con características observables del cliente, particularmente su antigüedad.

### Decisión preliminar

Se conservarán los registros durante el análisis exploratorio y no se realizará ninguna imputación en esta etapa.

Posteriormente, durante la Actividad 4, se compararán distintas estrategias de imputación numérica para determinar su impacto sobre la distribución de los datos y el desempeño del clasificador.

También se evaluará la conveniencia de crear un indicador binario de ausencia.

## 2.4. Declaración de asistencia de IA

Se utilizó ChatGPT como apoyo para ver ideas sobre el código de identificación de valores ausentes.

Los 11 registros afectados, sus valores de antigüedad y características contractuales fueron comprobados mediante la ejecución del análisis en Jupyter Notebook.

## 2.4. Detección de registros duplicados

```Resultados
- Total de registros: 7,043.
- Filas completamente duplicadas: 0.
- Identificadores customerID duplicados: 0.
- Identificadores customerID únicos: 7,043.
```

Los resultados de esta sección nos dieron que el dataseet contiene 7,043 registros y que dentro de estos registros no se encontraron filas que estén completamente duplicadas ni identificadores  repetidos. Con base en lo anterior es importante para mantener la integridad de los datos y evitar que un mismo cliente esté representado varias veces dentro del conjunto de datos.

como no se encontraron alguna duplicidad, no se ocupara aplicar la eliminación de duplicados. Por ende todos los registros se conservaran  

## 2.5. Estadísticas descriptivas

Se encontró que los clientes cuentan con una antiguedad de 32.7 meses, mientras que la mediana es de 29 meses. La desviación estándar de 24.56 meses indica que existe una variación considerable en el tiempo que los clientes llevan utilizando el servicio. Además, se observa que la antigüedad mínima es de 0 meses y la máxima de 72 meses.

**Análisis de** `MonthlyCharges`**:**

Los cargos mensuales presentan una media de 64.76 y una mediana de 70.35, con una desviación estándar de 30.09. Estos resultados muestran que los clientes pagan cantidades diferentes por sus servicios, posiblemente debido a los distintos planes y características contratadas. Sin embargo, sería necesario analizar otras variables para confirmar esta explicación.

La variable `SeniorCitizen` está representada mediante valores de 0 y 1, por lo que, aunque pandas la considera numérica, corresponde a una variable categórica binaria. Su media indica que aproximadamente el 16.21% de los clientes son adultos mayores.

Por otra parte, `TotalCharges` no aparece en las estadísticas descriptivas numéricas porque inicialmente está almacenada como texto. Será necesario realizar una conversión controlada para analizarla correctamente, considerando los 11 registros con valores vacíos identificados anteriormente.

### 2.6. Análisis de percentiles y asimetría

Los resultados muestran que la antigüedad de los clientes (`tenure`) presenta una asimetría positiva ligera de 0.239540, mientras que los cargos mensuales (`MonthlyCharges`) presentan una asimetría negativa ligera de -0.220524.

En el análisis de percentiles se observó que el 50% central de los clientes tiene una antigüedad comprendida entre 9 y 55 meses, mientras que los cargos mensuales del 50% central se encuentran entre 35.50 y 89.85.

Estos resultados indican que ambas variables presentan cierta asimetría y una dispersión considerable de sus valores. 

### 2.7. Análisis de frecuencias categóricas

Se analizaron las variables categóricas del dataset mediante la función `value_counts()` de pandas, con el objetivo de conocer la cantidad de registros correspondientes a cada categoría. También se utilizó `normalize=True` para calcular sus porcentajes y facilitar la comparación entre ellas.

**Análisis de la variable objetivo (**`**Churn**`**):**

Se identificó que el 73.46% de los clientes no canceló su servicio, mientras que el 26.54% sí lo hizo. Estos resultados muestran un desbalance entre las clases, ya que existe una mayor cantidad de clientes que permanecieron con la compañía.

**Análisis de contratos y servicios:**

Respecto al tipo de contrato, se observó que el 55.02% de los clientes cuenta con un contrato mensual, siendo la categoría más frecuente.

En cuanto al servicio de internet, el 43.96% utiliza fibra óptica, el 34.37% DSL y el 21.67% no tiene contratado este servicio.

Por otra parte, el método de pago más utilizado es el cheque electrónico, con un 33.58% de los clientes.

**Características generales de los clientes:**

La distribución por género es equilibrada, con un 50.48% de hombres y un 49.52% de mujeres. Además, el 16.21% de los clientes está clasificado como adulto mayor y el 29.96% tiene dependientes.

También se identificó que el 90.32% cuenta con servicio telefónico y el 59.22% utiliza facturación electrónica.

### 2.8. Detección de columnas constantes, valores inválidos y correlaciones

Durante el análisis se utilizó la función `nunique()` para identificar columnas constantes. Los resultados mostraron que ninguna de las 21 variables contiene un único valor, por lo que no es necesario descartar columnas por falta de variabilidad.

Posteriormente, se realizaron comprobaciones para detectar valores inválidos y posibles inconsistencias entre variables. No se encontraron antigüedades ni cargos mensuales negativos, tampoco valores fuera de las categorías permitidas para `SeniorCitizen`.

Asimismo, se verificó la consistencia entre los servicios contratados. No se identificaron inconsistencias en las combinaciones examinadas de servicios telefónicos y de internet.

Finalmente, se calculó la correlación de Pearson entre `tenure` y `MonthlyCharges`, obteniendo un coeficiente de 0.2479. Este resultado representa una correlación positiva débil, lo que sugiere que los clientes con mayor antigüedad tienden a presentar cargos mensuales ligeramente superiores, aunque la relación no es suficientemente fuerte para establecer una asociación lineal importante.
