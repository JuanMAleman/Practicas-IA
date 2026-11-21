# Prácticas de IA

https://github.com/JuanMAleman/Practicas-IA

En este repositorio se encuentran todas las prácticas que
se realizaran a lo largo del semestre 27/1 en la materia 
de inteligencia artificial en el grupo 6CV2.

### Integrantes de equipo

- Juan Manriquez [@JuanMAleman](https://github.com/JuanMAleman/)
- Cristopher De La O [@cdelaof26](https://github.com/cdelaof26/)
- José Omar Aguilar [@Jose-omar-aguilar](https://github.com/Jose-omar-aguilar)
- Ana Fabiola Robles [@FabsRobles](https://github.com/FabsRobles)
- Axel Paredes  [@A-20AA](https://github.com/A-20AA)

# Práctica 4. Redes Neuronales Convolucionales en CPU o GPU de gama baja

## Descripción

Este proyecto tiene como objetivo implementar una red neuronal convolucional (CNN) pequeña en PyTorch para clasificar imágenes de Fashion-MNIST, compararla contra una línea base sin convoluciones (MLP) y evaluar su desempeño y costo computacional en equipos con recursos limitados (CPU o GPU de gama baja).

## Objetivos

- Implementar una CNN pequeña en PyTorch y calcular a mano el número de parámetros de cada capa.
- Escribir y depurar un ciclo de entrenamiento y evaluación (pérdida, retropropagación, optimizador).
- Diseñar un experimento controlado variando un solo factor (ancho, kernel, normalización, regularización o aumento de datos).
- Distinguir entre conjunto de entrenamiento, validación y prueba, respetando la regla de usar la prueba una sola vez.
- Interpretar el modelo mediante matriz de confusión, errores típicos, filtros y mapas de activación.
- Medir el costo computacional (parámetros y segundos por época) y decidir con criterios de eficiencia.

## Tecnologías

- Python 3.10
- Visual Studio Code
- Jupyter Notebook
- PyTorch y torchvision
- NumPy y Matplotlib

## Estructura del proyecto

- `cnn_lab_scaffold.py`: código base de la práctica con los bloques completados.
- `cnn_lab.ipynb`: notebook con la ejecución y el análisis de cada parte.
- `outputs/`: figuras y resultados generados (muestras, curvas, tablas en JSON).
- `data/`: Fashion-MNIST descargado automáticamente (≈ 30 MB).

## Instalación y reproducción

1. Clonar el repositorio.
2. Abrir la carpeta de la práctica en VS Code.
3. Crear un entorno virtual con `python -m venv .venv`.
4. Activar el entorno virtual.
5. Instalar las dependencias con `python -m pip install torch torchvision matplotlib numpy`.
6. Verificar el entorno con `python cnn_lab_scaffold.py --part data --fake`.
7. Abrir `cnn_lab.ipynb`, seleccionar el kernel del entorno virtual y ejecutar las celdas en orden.

Si el equipo es lento, se puede agregar `--subset 10000` o `--threads N`. Las opciones usadas en cada experimento se declaran en el notebook.

## Dataset

Fashion-MNIST: 70,000 imágenes en escala de grises de 28×28 píxeles y 10 clases de prendas. Se usa la partición 55,000 imágenes de entrenamiento, 5,000 de validación y 10,000 de prueba, con semilla fija para la separación entrenamiento/validación.

## Metodología

El trabajo se divide en cuatro partes:

1. **Exploración de datos:** revisión de muestras, partición y normalización.
2. **Línea base y primera CNN:** implementación de `SimpleCNN` (105,866 parámetros) y comparación contra un MLP (109,386 parámetros) en exactitud, parámetros y segundos por época. Se evalúa la variación entre semillas para decidir cuándo una diferencia es real.
3. **Experimento controlado:** variación de un solo factor y análisis de su efecto.
4. **Evaluación final e interpretación:** exactitud en prueba, matriz de confusión, filtros y mapas de activación.

## Resultados

