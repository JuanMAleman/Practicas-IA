# Actividad 1. Comprensión del dominio del dataset

## 1.1. Descripción general

El conjunto de datos **Telco Customer Churn** contiene información sobre clientes de una empresa de telecomunicaciones, incluyendo características demográficas, servicios contratados, modalidades de facturación y permanencia.

Su análisis tiene como finalidad estudiar los factores asociados al abandono del servicio y preparar los datos para desarrollar un modelo de clasificación binaria.

## 1.2. Características del dataset

|Característica|Descripción|
|---|---|
|Nombre|Telco Customer Churn|
|Fuente|IBM|
|Formato|CSV|
|Número de observaciones|7,043|
|Número de atributos|21 columnas, incluida la variable objetivo|
|Unidad de análisis|Cliente registrado en el conjunto de datos|
|Variable objetivo|Churn|
|Tipo de problema|Clasificación binaria|

## 1.3. Variable objetivo

La variable `Churn` indica si un cliente ha abandonado el servicio.

- **Yes:** el cliente abandonó el servicio.
    
- **No:** el cliente no abandonó el servicio.
    

En un escenario de aplicación real, esta variable sería el resultado que el modelo intentaría predecir utilizando información disponible antes del abandono.

## 1.4. Identificación preliminar de los atributos

El dataset contiene información relacionada con:

- **Características demográficas:** género, condición de adulto mayor, pareja y dependientes.
    
- **Servicios contratados:** telefonía, internet, soporte técnico, seguridad y servicios adicionales.
    
- **Información contractual:** tipo de contrato, facturación y método de pago.
    
- **Información económica y temporal:** antigüedad, cargos mensuales y cargos totales.
    
## 1.4.1. Diccionario de datos

| Atributo           | Descripción                                | Tipo conceptual                           |
| ------------------ | ------------------------------------------ | ----------------------------------------- |
| `customerID`       | Identificador único del cliente            | Identificador                             |
| `gender`           | Género registrado                          | Categórica                                |
| `SeniorCitizen`    | Indica si es adulto mayor (0 = No, 1 = Sí) | Categórica binaria                        |
| `Partner`          | Indica si tiene pareja                     | Categórica                                |
| `Dependents`       | Indica si tiene dependientes               | Categórica                                |
| `tenure`           | Meses de permanencia como cliente          | Numérica discreta                         |
| `PhoneService`     | Contratación de servicio telefónico        | Categórica                                |
| `MultipleLines`    | Disponibilidad de múltiples líneas         | Categórica                                |
| `InternetService`  | Tipo de servicio de internet               | Categórica                                |
| `OnlineSecurity`   | Contratación de seguridad en línea         | Categórica                                |
| `OnlineBackup`     | Contratación de respaldo en línea          | Categórica                                |
| `DeviceProtection` | Contratación de protección de dispositivos | Categórica                                |
| `TechSupport`      | Contratación de soporte técnico            | Categórica                                |
| `StreamingTV`      | Contratación de televisión por streaming   | Categórica                                |
| `StreamingMovies`  | Contratación de películas por streaming    | Categórica                                |
| `Contract`         | Modalidad o duración del contrato          | Categórica                                |
| `PaperlessBilling` | Uso de facturación electrónica             | Categórica                                |
| `PaymentMethod`    | Método de pago utilizado                   | Categórica                                |
| `MonthlyCharges`   | Importe mensual facturado                  | Numérica continua                         |
| `TotalCharges`     | Importe total facturado                    | Numérica continua (almacenada como texto) |
| `Churn`            | Indica si abandonó el servicio             | Variable objetivo binaria                 |
## 1.5. Hallazgos iniciales

Durante la inspección preliminar se identificaron los siguientes aspectos:

1. `customerID` funciona como identificador del cliente y no representa directamente una característica predictiva.
    
2. `SeniorCitizen` aparece como dato numérico, pero representa una categoría binaria.
    
3. `TotalCharges` se interpreta inicialmente como texto, aunque representa un importe económico. Se requiere investigar la causa antes de realizar conversiones.
    
4. Algunas variables incluyen categorías como `No phone service`, que representan la ausencia de contratación de un servicio y no deben confundirse con valores faltantes.
    

## 1.6. Consideraciones pendientes

Se requiere completar la revisión de:

- Licencia y condiciones de utilización del dataset.
    
- Significado y dominio de todos los atributos.
    
- Identificadores y posibles fugas de información.
    
- Disponibilidad temporal de las variables predictoras.
    
- Riesgos éticos y decisiones que podrían afectar desigualmente a distintos grupos.
    

## 1.7. Uso de inteligencia artificial

Se utilizó ChatGPT como herramienta de apoyo para estructurar el procedimiento exploratorio, explicar el código Python y organizar la documentación inicial.

Las dimensiones del dataset, tipos de datos y categorías descritas fueron comprobadas mediante la ejecución de código en Jupyter Notebook. Las decisiones de preprocesamiento y las conclusiones del análisis quedan pendientes de verificación.

## 1.8. Unidad de análisis, disponibilidad de la variable objetivo y riesgos

### Unidad de análisis

Cada fila representa el registro de un cliente de una empresa de telecomunicaciones, incluyendo información demográfica, contractual, servicios contratados, antigüedad y cargos facturados.

### Disponibilidad de la variable objetivo

La variable `Churn` indica si el cliente abandonó el servicio. En una aplicación predictiva real, esta información solamente estaría disponible después de observar el abandono durante un periodo definido.

Por lo tanto, para predecir el abandono futuro, el modelo deberá utilizar variables disponibles antes del evento y no información obtenida posteriormente.

### Identificadores y posibles fugas de información

El atributo `customerID` funciona como identificador del cliente. Se propone excluirlo de las variables predictoras, conservándolo únicamente para identificación y trazabilidad de registros cuando corresponda.

Las variables `tenure` y `TotalCharges` requieren especial atención porque sus valores pueden depender del momento en que se realiza la predicción. Se deberá comprobar que correspondan a información disponible antes del abandono.

La variable `Churn` se utilizará exclusivamente como objetivo de clasificación.

### Riesgos éticos

El dataset incluye información demográfica, como el género y la condición de adulto mayor, que podría estar relacionada con diferencias en el comportamiento de los clientes o en las decisiones comerciales.

El uso de modelos predictivos deberá considerar posibles diferencias de desempeño entre grupos. En particular, se recomienda evaluar métricas de clasificación desagregadas para identificar diferencias relevantes en errores, sensibilidad y precisión.

### Posibles decisiones con impacto desigual

Las predicciones podrían utilizarse para ofrecer promociones, priorizar atención o implementar estrategias de retención.

Sin controles adecuados, algunos grupos podrían recibir menos beneficios o ser clasificados incorrectamente con mayor frecuencia.

Por ello, las decisiones basadas en el modelo deben contar con criterios transparentes y mecanismos de evaluación de resultados entre grupos.

### Limitaciones

El dataset no proporciona por sí solo toda la información temporal y contextual necesaria para demostrar que las variables predictoras estarían disponibles en el momento de uso. Estas restricciones deberán reconocerse al interpretar los resultados.

No se asumirán relaciones causales a partir de asociaciones estadísticas.

## 1.9. Fuente, licencia y procedencia del dataset

### Fuente original

El dataset **Telco Customer Churn** se obtuvo del repositorio público de IBM denominado _telco-customer-churn-on-icp4d_, desarrollado como ejemplo de análisis de datos y predicción del abandono de clientes mediante técnicas de aprendizaje automático.

**Repositorio:** [https://github.com/IBM/telco-customer-churn-on-icp4d](https://github.com/IBM/telco-customer-churn-on-icp4d)

**Archivo original:** [https://github.com/IBM/telco-customer-churn-on-icp4d/blob/master/data/Telco-Customer-Churn.csv](https://github.com/IBM/telco-customer-churn-on-icp4d/blob/master/data/Telco-Customer-Churn.csv)

**Formato:** CSV.

**Dimensiones verificadas:** 7,043 registros y 21 columnas.

### Licencia y condiciones de uso

El proyecto de IBM se distribuye bajo la licencia Apache License 2.0. Sin embargo, la documentación del repositorio señala que los componentes de terceros pueden estar sujetos a licencias independientes y no establece expresamente una licencia diferenciada para el archivo CSV.

Por esta razón, se reconoce la procedencia original del dataset y se evita asumir derechos de redistribución adicionales no documentados.

### Reproducibilidad y conservación de datos

El archivo original se conserva dentro de la carpeta `datasets/` del proyecto, sin modificaciones.

Las transformaciones y estrategias de preparación se implementarán mediante código Python en Jupyter Notebook, permitiendo identificar los cambios y reproducir los experimentos.

El código y la documentación se mantendrán en el repositorio GitHub de la práctica.

### Referencia

IBM. _Predict Customer Churn using Watson Machine Learning and Jupyter Notebooks on Cloud Pak for Data_. GitHub. [https://github.com/IBM/telco-customer-churn-on-icp4d](https://github.com/IBM/telco-customer-churn-on-icp4d)