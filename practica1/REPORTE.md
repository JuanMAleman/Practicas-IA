# Reporte de práctica

## Estructura del proyecto

El proyecto tiene diferentes directorios y archivos,
- `src`: Contiene los archivos de las diferentes secciones
- `src/tests`: Contiene tests escritos con `pytest` para cada 
  sección, estos contrastas los resultados de los ejemplos vistos 
  en clase con los arrojados por el algoritmo implementado 
- `main.py`: Punto de entrada, más información en [README.md](README.md)

## Pruebas unitarias

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

## Contenidos y algunas decisiones de diseño

### main.py

En `main.py` se utiliza un `parser` de argumentos CLI con el fin de 
facilitar la ejecución de las diferentes secciones y si se quieren
cambiar parámetros de ejecución o realizar las pruebas unitarias.

### metrics.py

`metrics.py` contiene todos los parámetros necesarios para dar un
reporte de ejecución.

### map_download.py

Pequeño archivo con una única tarea: traer grafo de algún sitio,
que puede ser especificado por CLI, utilizando el módulo de `osmnx`.


## Sección 1: Búsqueda a ciegas

En esta sección se implementó un algoritmo "genérico" que 
simplemente cambia la estructura de datos en función del 
algoritmo que se quiere ejecutar.

### s1.py

Archivo principal de la sección 1. En esta sección se encuentran 
diferentes clases y funciones,

- `Algorithm(Enum)`: enum que tiene un listado de los algoritmos 
  que se pueden utilizar con la clase `UFSA`
- `UFSA(Metrics)`: "Uninformed Search Algorithms" es la clase que
  implementa un único algoritmo de búsqueda no informada que cambia
  la estructura de datos con base en el algoritmo seleccionado.
- `plot_graph(...)`: función que gráfica el grafo, utiliza diferentes 
  colores para distinguir entre el nodo inicial (verde), 
  nodo final (azul) y los nodos de frontera (naranja).
- `run(**kwargs)`: punto de entrada que orquesta la ejecución de los
  algoritmos. La función anidada `plot_snapshots(ufsa: UFSA)`, 
  utiliza `multiprocessing` para mostrar los tres momentos de la 
  frontera al mismo tiempo en diferentes ventanas, `matplotlib` no
  es _thread-safe_, por lo que `threading` no es compatible.

## Pruebas con grafos con `osmnx`

Las pruebas se ejecutaron con la Escuela Superior de Cómputo como
epicentro, y con todos los nodos a una distancia de 2 km, utilizando
el siguiente comando,

```shell
python3 main.py s1 --distance 2000 --graph
```

### Hardware y software

| Nombre  | Valor                  |
|---------|------------------------|
| CPU     | Apple M4 de 10 núcleos |
| Memoria | 16 GB LPDDR5           |
| OS      | macOS 15.7.4           |
| Python  | v3.14.6:c63aec69bd5    |


### Ejecución de BFS

<pre>
Reporte de BFS
  Nodo inicial:     94144498
  Nodo final:       1588601898
  Nodos totales:    476
  Ruta:             94144498 → 17809170 → 94143538 → 9300602214 → 17809166 → 5749702260 → 151354808 → 152737653 → 152737652 → 2175327576 → 1588595442 → 1588595435 → 1588601898
  Nodos expandidos: 1470
  Distancia total:  1606.1046201895174
  Total de arcos:   12
    Tamaño de
  frontera máximo:  848
    Tiempo de
    ejecución:      4.3967 ms 
</pre>

| Frontera 1            | Frontera 2            | Frontera 3            |
|-----------------------|-----------------------|-----------------------|
| ![F1](img/BFS_F1.png) | ![F2](img/BFS_F2.png) | ![F3](img/BFS_F3.png) |


### Ejecución de DFS

<pre>
Reporte de DFS
  Nodo inicial:     94144498
  Nodo final:       1588601898
  Nodos totales:    476
  Ruta:             94144498 → 17809163 → 367967 → 151357427 → 151357502 → 25034664 → 5116936565 → 704766 → 151358603 → 13336347838 → 151360584 → 256409832 → 256409987 → 256409741 → 1761555130 → 34674622 → 34674624 → 34151805 → 430788 → 5773573552 → 151361754 → 151361175 → 256413458 → 5749702259 → 5749702260 → 151354808 → 152738277 → 152737902 → 406653331 → 152737653 → 152737652 → 152737125 → 94141096 → 152739331 → 2175327576 → 1588595442 → 1588595435 → 697813609 → 573458028 → 573458029 → 26401805 → 26666918 → 218155202 → 26666919 → 1588601898
  Nodos expandidos: 12994
  Distancia total:  4263.216671449974
  Total de arcos:   44
    Tamaño de
  frontera máximo:  31
    Tiempo de
    ejecución:      58.2731 ms 
</pre>

| Frontera 1            | Frontera 2            | Frontera 3            |
|-----------------------|-----------------------|-----------------------|
| ![F1](img/DFS_F1.png) | ![F2](img/DFS_F2.png) | ![F3](img/DFS_F3.png) |


### Ejecución de UCS

<pre>
Reporte de UCS
  Nodo inicial:     94144498
  Nodo final:       1588601898
  Nodos totales:    476
  Ruta:             94144498 → 17809170 → 94144708 → 94143743 → 94145388 → 94140737 → 94143863 → 94139827 → 94139897 → 94139728 → 178889521 → 152737125 → 94141096 → 152739331 → 227073732 → 1588601898
  Nodos expandidos: 2228
  Distancia total:  1056.1395886679431
  Total de arcos:   15
    Tamaño de
  frontera máximo:  1202
    Tiempo de
    ejecución:      13.0460 ms 
</pre>

| Frontera 1            | Frontera 2            | Frontera 3            |
|-----------------------|-----------------------|-----------------------|
| ![F1](img/UCS_F1.png) | ![F2](img/UCS_F2.png) | ![F3](img/UCS_F3.png) |



### Ejecución de fallida de BFS

Las siguientes pruebas fallaron porque el algoritmo no fue capaz
de encontrar una ruta entre los nodos de inicio y fin, incluso si
el timeout se cambia a 10 s, esto debido a la desconexión entre 
nodos.

<pre>
Reporte de BFS
  Nodo inicial:     35514154
  Nodo final:       431394905
  Nodos totales:    476
  Ruta:             
  Nodos expandidos: 816200
  Distancia total:  No termino,
  Total de arcos:   timeout de 3s
    Tamaño de
  frontera máximo:  402219
    Tiempo de
    ejecución:      3.0059 s 
</pre>

| Frontera 1              | Frontera 2              | Frontera 3              |
|-------------------------|-------------------------|-------------------------|
| ![F1](img/f/BFS_F1.png) | ![F2](img/f/BFS_F2.png) | ![F3](img/f/BFS_F3.png) |


### Ejecución de fallida de DFS

<pre>
Reporte de DFS
  Nodo inicial:     35514154
  Nodo final:       431394905
  Nodos totales:    476
  Ruta:             
  Nodos expandidos: 825132
  Distancia total:  No termino,
  Total de arcos:   timeout de 3s
    Tamaño de
  frontera máximo:  85
    Tiempo de
    ejecución:      3.0000 s 
</pre>

| Frontera 1              | Frontera 2              | Frontera 3              |
|-------------------------|-------------------------|-------------------------|
| ![F1](img/f/DFS_F1.png) | ![F2](img/f/DFS_F2.png) | ![F3](img/f/DFS_F3.png) |


### Ejecución de fallida de UCS

<pre>
Reporte de UCS
  Nodo inicial:     35514154
  Nodo final:       431394905
  Nodos totales:    476
  Ruta:             
  Nodos expandidos: 648370
  Distancia total:  No termino,
  Total de arcos:   timeout de 3s
    Tamaño de
  frontera máximo:  310714
    Tiempo de
    ejecución:      3.0694 s 
</pre>

| Frontera 1              | Frontera 2              | Frontera 3              |
|-------------------------|-------------------------|-------------------------|
| ![F1](img/f/UCS_F1.png) | ![F2](img/f/UCS_F2.png) | ![F3](img/f/UCS_F3.png) |


## Preguntas de análisis

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


## Referencias

Uso de heapq y queue
- https://docs.python.org/3/library/heapq.html#basic-examples
- https://docs.python.org/3.14/library/queue.html

Uso de osmnx
- https://osmnx.readthedocs.io/en/stable/user-reference.html

Uso de argparse
- https://docs.python.org/3.14/library/argparse.html

Algoritmos DFS, BFS y UCS
- Programa web proporcionado: `busqueda_no_informada.html`

Otra documentación consultada
- https://tedboy.github.io/networkx/reference/graph_types.multidigraph.html
- https://www.openstreetmap.org/node/11359618606#map=19/19.504152/-99.147103
- https://networkx.org/documentation/stable/auto_examples/drawing/plot_weighted_graph.html
- https://matplotlib.org/stable/gallery/shapes_and_collections/fancybox_demo.html
- https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution
- https://github.com/gboeing/osmnx-examples
- https://www.geeksforgeeks.org/python/stack-in-python/
- https://stackoverflow.com/questions/34764535/why-cant-matplotlib-plot-in-a-different-thread
- https://docs.python.org/3.14/library/multiprocessing.html#multiprocessing.Process
