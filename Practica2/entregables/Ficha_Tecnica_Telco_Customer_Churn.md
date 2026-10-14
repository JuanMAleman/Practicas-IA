# Ficha técnica del dataset: Telco Customer Churn

## 1. Identificación del dataset

**Nombre:** Telco Customer Churn  
**Fuente:** IBM  
**Repositorio:** [https://github.com/IBM/telco-customer-churn-on-icp4d](https://github.com/IBM/telco-customer-churn-on-icp4d)  
**Archivo:** `Telco-Customer-Churn.csv`  
**Tipo de problema:** Clasificación binaria supervisada  
**Unidad de análisis:** Cliente de una empresa de telecomunicaciones  
**Dimensiones:** 7,043 registros y 21 columnas
## 2. Descripción y variables

El dataset contiene información sobre características demográficas, servicios contratados, condiciones comerciales y facturación de clientes de telecomunicaciones.

La variable objetivo es `Churn`, que indica si un cliente canceló (`Yes`) o no (`No`) su servicio.

Se identificaron 19 variables predictoras después de excluir `customerID`, por ser un identificador único, y `Churn`, por ser la variable objetivo.

Entre las variables principales destacan:

- **Numéricas:** `tenure` (antigüedad en meses), `MonthlyCharges` (cargos mensuales) y `TotalCharges` (cargos acumulados).
    
- **Categóricas:** `Contract`, `InternetService`, `PaymentMethod`, `gender` y `SeniorCitizen`, entre otras.
Aunque `SeniorCitizen` está almacenada como entero, representa una variable categórica binaria.
## 3. Diagnóstico de calidad de datos

Se identificaron 11 valores vacíos en `TotalCharges`, equivalentes aproximadamente al 0.16% de los registros. Estos valores estaban representados mediante espacios en blanco y requirieron una conversión a valores ausentes reconocidos por pandas.

Los 11 registros afectados presentaban `tenure = 0`.

No se encontraron registros completamente duplicados, identificadores `customerID` repetidos ni columnas constantes.

Tampoco se identificaron valores negativos en `tenure` o `MonthlyCharges`, ni inconsistencias en las relaciones de servicios verificadas durante el Data Profiling.
## 4. Distribución y características estadísticas

La variable objetivo presenta la siguiente distribución:

|Clase|Registros|Porcentaje|
|---|---|---|
|No|5,174|73.46%|
|Yes|1,869|26.54%|

La razón de desbalance es aproximadamente 2.77, superior al umbral de 1.5 establecido en la práctica.

El análisis exploratorio identificó una relación entre el tipo de contrato y la cancelación: los clientes con contratos mensuales presentaron una tasa de cancelación del 42.71%, frente al 2.83% de quienes tenían contratos de dos años.

También se observó que los clientes que cancelaron generalmente presentaban menor antigüedad y cargos mensuales más elevados.
## 5. Preparación de los datos

Se compararon estrategias de imputación por media, mediana y regla de dominio para `TotalCharges`. Se seleccionó la mediana como alternativa de referencia, debido a su resistencia frente a valores extremos y su desempeño predictivo comparable.

Para estudiar la imputación categórica se simularon ausencias controladas en `Contract`, comparando moda y categoría `Desconocido`.

Se aplicaron dos criterios de winsorización: IQR y percentiles P5–P95. El primero no modificó observaciones; el segundo alteró valores potencialmente válidos sin producir mejoras predictivas relevantes. Por ello, se decidió conservar los datos sin winsorización.

Finalmente, se compararon estrategias de sobremuestreo aleatorio, submuestreo aleatorio y SMOTENC. Se seleccionó provisionalmente el submuestreo por su capacidad para identificar cancelaciones.

Las evaluaciones se realizaron utilizando validación cruzada estratificada y pipelines para evitar fugas de información.
