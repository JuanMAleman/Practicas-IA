# Reporte de práctica

### Estructura del proyecto

El proyecto tiene diferentes directorios y archivos,
- `src`: Contiene los archivos de las diferentes secciones
- `src/tests`: Contiene tests escritos con `pytest` para cada 
  sección, estos contrastas los resultados de los ejemplos vistos 
  en clase con los arrojados por el algoritmo implementado 
- `main.py`: Punto de entrada, más información en [README.md](README.md)

### Sección 1: Búsqueda a ciegas

En esta sección se implementó un algoritmo "genérico" que 
simplemente cambia la estructura de datos en función del 
algoritmo que se quiere ejecutar.

### Pruebas unitarias

Las pruebas unitarias prueban la funcionalidad del método 
`perform_search` contrastando los resultados del programa en 
`busqueda_no_informada.html`.

Los resultados de DFS y BFS discrepan entre el algoritmo 
implementado y el programa de `busqueda_no_informada.html`, 
esto se debe al cómo funcionan los diccionarios de datos en 
Python. En `s1_test` los datos del grafo están descritos en un
diccionario de datos, estructura que automáticamente ordena las
llaves, esto tiene como consecuencia que los nodos se insertan 
de forma ordenada, por lo que al momento de ejecutar el algoritmo
los nodos adjacentes se exploran de esta forma, esto no 
necesariamente sucede en el programa de `busqueda_no_informada.html`.

### Contenidos y algunas decisiones de diseño

#### main.py

En `main.py` se utiliza un `parser` de argumentos CLI con el fin de 
facilitar la ejecución de las diferentes secciones y si se quieren
cambiar parámetros de ejecución o realizar las pruebas unitarias.

#### metrics.py

`metrics.py` contiene todos los parámetros necesarios para dar un
reporte de ejecución.

#### map_download.py

Pequeño archivo con una única tarea: traer grafo de algún sitio,
que puede ser especificado por CLI, utilizando el módulo de `osmnx`.

#### s1.py

Archivo principal de la sección 1. En esta sección se encuentran 
diferentes clases y funciones,

- `Algorithm(Enum)`: enum que tiene un listado de los algoritmos 
  que se pueden utilizar con la clase `UFSA`
- `UFSA(Metrics)`: "Uninformed Search Algorithms" es la clase que
  implementa los tres algoritmos de búsqueda no informada. 

### Pruebas con grafos con `osmnx`

### Preguntas de análisis

- **¿Por qué BFS garantiza el camino con menos saltos pero no el de menor distancia?**

Esto es porque en algunos grafos existen diferentes rutas de un 
nodo de inicio a uno final, pero no todas tienen el mismo costo 
acumulado, por lo que aunque se BFS da el camino con menos saltos, 
no toma en cuenta el peso para decidir por un camino u otro.

- **¿En qué estructuras de grafo DFS es preferible? ¿Aplica en este caso urbano?**

Las estructuras deben ser grafos completos, ya que si existen 
conjuntos de nodos no conectados y el nodo de inicio o final 
están en estos subconjuntos, el algoritmo no podrá encontrar 
el otro nodo. Los grafos urbanos no siempre cumplen la condición 
de ser completos.

- **¿Cuándo UCS y BFS producen exactamente el mismo resultado?**

Producen el mismo resultado cuando el camino de menos arcos (BFS)
es el mismo que el de menor costo (UCS).
