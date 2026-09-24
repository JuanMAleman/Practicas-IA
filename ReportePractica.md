# Reporte de Práctica: Algoritmos de Búsqueda Informada (A* y Greedy Best-First)

## Resumen

El siguiente reporte de practica documenta la implementación, evaluación y análisis empírico del algoritmo de búsqueda A* utilizando diferentes funciones heurísticas del tipo A*, en comparación con Greedy Best-First Search (GBFS). Se evalúa el desempeño de las heurísticas en términos de nodos expandidos, costo del camino y tiempo de ejecución; además el Factor de ramificación efectiva b* en los resultados nos muestra la eficiencia que tiene cada algoritmo en el control de espacio de busqueda. Cada uno de los datos anteriores se calcula sobre un grafo urbano extraído de OpenStreetMap. Los resultados demuestran que el uso de una heurística admisible y consistente reduce el espacio de búsqueda explorado manteniendo la optimalidad del costo del camino.

## 1. Objetivos

### 1 Objetivo General

Implementar A* con múltiples heurísticas geográficas y demostrar empíricamente que una heurística
admisible reduce los nodos expandidos respecto a UCS sin comprometer la optimalidad del camino.

### 2 Tareas requeridas

- Implementar A* apoyado en una cola de prioridad que ordene por $f(n) = g(n) + h(n)$.
- Definir e implementar tres heurísticas geográficas: Distancia Euclidiana ($h_1$), Distancia de Haversine ($h_2$) y una heurística personalizada ($h_3$).
- Verificar la admisibilidad de cada heurística de forma experimental o teorica que $h(n) <= costo real minimo$.
- Implementar el algoritmo Greedy Best-First Search y comparar contra A* para ilustrar no-optimalidad.
- Medir la calidad informativa de las heurísticas mediante el factor de ramificación efectiva ($b^*$).
- Visualizar interactivamente las rutas generadas sobre el mapa urbano utilizando la librería `folium`.
- Construir tablas comparativas.
## 2. Marco Teórico y Justificación de Heurísticas

### 2.1 Algoritmos de Búsqueda

**A\* Search:** Algoritmo de búsqueda informada que selecciona el siguiente nodo a expandir según la función de evaluación $f(n) = g(n) + h(n)$, donde $g(n)$ es el costo acumulado que suma cada nodo que se explora(puede ser parte de la solucion final o no) desde el origen hasta el nodo $n$, y $h(n)$ es la estimación del costo restante hasta el destino(costo calculado en linea recta desde el nodo actual hasta el nodo objetivo).

**Greedy Best-First Search (GBFS):** Búsqueda informada que evalúa nodos únicamente por $f(n) = h(n)$. Prioriza la cercanía aparente a la meta sin considerar el costo acumulado $g(n)$, lo que puede provocar una solución que no es la más optima a cambio de velocidad.

### 2.2 Definición de Heurísticas Implementadas

**$h_1$ — Distancia Euclidiana (Proyectada)**

Calcula la línea recta cartesiana considerando las coordenadas proyectadas $(x_n, y_n)$ y $(x_d, y_d)$, lo que provoca una distancia teorica ideal(no se toma en cuenta la curvatura de la tierra):

$$h_1(n) = \sqrt{(x_d - x_n)^2 + (y_d - y_n)^2}$$

**$h_2$ — Distancia de Haversine**

Calcula el camino más corto a lo largo de la superficie de una esfera (distancia ortodrómica) a partir de las coordenadas en latitud y longitud $(\phi, \lambda)$ expresadas en radianes:

$$h_2(n) = 2R \cdot \arcsin\left( \sqrt{\sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_n)\cos(\phi_d)\sin^2\left(\frac{\Delta \lambda}{2}\right)} \right)$$

donde $R \approx 6{,}371{,}000\ \text{m}$ es el radio medio terrestre.

**$h_3$ — Heurística Personalizada (Distancia + Estimación de Giros)**

Diseñada para modelar el costo en redes viales combinando la distancia de Haversine con una penalización estimada por cambios de dirección hacia el nodo destino:

$$h_3(n) = h_2(n) + \alpha \cdot \theta(n)$$

donde $\theta(n)$ estima la desviación angular respecto al vector hacia la meta y $\alpha$ es un parámetro de ponderación ajustable.

## 3. Demostración de Admisibilidad y Consistencia

Para garantizar la optimalidad de A* en grafos de estado, la heurística $h(n)$ debe ser **admisible**: nunca debe sobreestimar el costo real para alcanzar la meta desde ningún nodo $n$, en la exploración de nodos cuando esto sucede ese nodo se excluye de la solución y el algoritmo continua explorando otros nodos para encontrar la solución más optima.

$$h(n) \le h^*(n) \quad \forall n$$

### 3.1 Análisis de Admisibilidad de $h_1$ y $h_2$

- **$h_2$ (Haversine):** Representa la distancia geodésica mínima en línea recta sobre la esfera terrestre entre el nodo $n$ y el destino. Como ningún camino físico por calles terrestres puede ser más corto que la línea recta geográfica que une ambos puntos, se cumple estrictamente $h_2(n) \le h^*(n)$. Por lo tanto, $h_2$ es admisible y consistente.

- **$h_1$ (Euclidiana):** En la impresion de la solucion en el grafo dado esta se muestra igual a haversine, y a la solucion ponderada, sin embargo tenemos un porcentaje de error en las distancias que se comprueba por nuestra distancia calculada entre nuestros nodos empresa y destinos conectados con lineas rectas, dado que los costos de cada arista nos los da por defecto openstreetmap con valores reales(curvatura terrestre) la solución se nos da con ese costo total. Sin embargo es calculable por el porcentaje de diferencia dado el valor real de la solucion de manera euclidiana.

### 3.2 Análisis de $h_3$ (Heurística Ponderada)

Si $\alpha > 0$, la adición de la estimación de giros puede ocasionar que en algunos casos $h_3(n) > h^*(n)$ (por ejemplo, si el camino real requiere giros que acortan el tiempo o si sobreestima el costo de maniobra). Si $h_3(n)$ sobreestima el costo real, deja de ser admisible y A* pierde la garantía teórica de encontrar el camino estrictamente óptimo.

## 4. Pruebas Experimentales y Resultados

Las pruebas se ejecutaron sobre un subgrafo urbano extraído mediante OSMnx, las zonas que comprenden el grafo(Cuauhtémoc, Gustavo A. Madero, Venustiano Carranza y Azcapotzalco) fueron delimitadas a un espacio de pruebas elegido de manera random con los siguientes valores(500 y 1500 nodos con 1 empresa y 20 destinos, 500 nodos con 1 empresa y 99 destino y 1500 con 1 empresa y 299 destino).

### 4.1 Tabla Comparativa de Desempeño

*1er ejecución* pytest -v -s

Prueba 500 nodos, 1 empresa, 19 destinos.

Distancia euclidiana(directa) total = 14254.40m

Distancia Haversine(directa) total = 14279.45m

| Algoritmo / Heurística | Distancia en metros | Nodos expandidos | Tiempo de Ejecución (ms) | Factor $b^*$ | Cantidad de nodos de la solución
|---|---|---|---|---|---|
| A* $h_1$ (Euclidiana) | 16967.05 | 745 | 14.03 | 1.013 | 179
| A* $h_2$ (Haversine) | 16967.05 | 745 | 19.37 | 1.013 | 179
| A* $h_3$ (Personalizada) | 16967.05 | 896 | 17.69 | 1.015 | 179
| Greedy Best-First | 17222.35 | 310 | 3.10 | 1.005 | 183 

Prueba 1500 nodos, 1 empresa, 19 destinos.

Distancia euclidiana(directa) total = 15195.42m

Distancia Haversine(directa) total = 15222.12m

| Algoritmo / Heurística | Distancia en metros | Nodos expandidos | Tiempo de Ejecución (ms) | Factor $b^*$ | Cantidad de nodos de la solución
|---|---|---|---|---|---|
| A* $h_1$ (Euclidiana) | 25615.97 | 1007 | 16.93 | 1.009 | 251
| A* $h_2$ (Haversine) | 25615.97 | 1004 | 27.20 | 1.009 | 251
| A* $h_3$ (Personalizada) | 25615.97 | 1468 | 23.23 | 1.012 | 251
| Greedy Best-First | 25615.97 | 567 | 5.00 | 1.004 | 286

Prueba 500 nodos, 1 empresa, 99 destinos.

Distancia euclidiana(directa) total = 21669.60m

Distancia Haversine(directa) total = 21707.68m

| Algoritmo / Heurística | Distancia en metros | Nodos expandidos | Tiempo de Ejecución (ms) | Factor $b^*$ | Cantidad de nodos de la solución
|---|---|---|---|---|---|
| A* $h_1$ (Euclidiana) | 39834.01 | 1857 | 69.12 | 1.003 | 590
| A* $h_2$ (Haversine) | 39834.01 | 1847 | 120.78 | 1.003 | 590
| A* $h_3$ (Personalizada) | 39772.99 | 2448 | 89.86 | 1.004 | 599
| Greedy Best-First | 41404.32 | 1043 | 21.63 | 1.002 | 594

Prueba 1500 nodos, 1 empresa, 299 destinos.

Distancia euclidiana(directa) total = 42428.53m

Distancia Haversine(directa) total = 42503.10m

| Algoritmo / Heurística | Distancia en metros | Nodos expandidos | Tiempo de Ejecución (ms) | Factor $b^*$ | Cantidad de nodos de la solución
|---|---|---|---|---|---|
| A* $h_1$ (Euclidiana) | 94784.03 | 4022 | 278.10 | 1.002 | 1249
| A* $h_2$ (Haversine) | 94784.03 | 4012 | 637.76 | 1.002 | 1249
| A* $h_3$ (Personalizada) | 96620.83 | 4853 | 348.54 | 1.002 | 1281
| Greedy Best-First | 97455.00 | 2701 | 144.67 | 1.001 | 1273

_______________________________________________________________________________________________________________________

*2da ejecución* pytest -v -s

Prueba 500 nodos, 1 empresa, 19 destinos.

Distancia euclidiana(directa) total = 13228.52m

Distancia Haversine(directa) total = 13251.77m

| Algoritmo / Heurística | Distancia en metros | Nodos expandidos | Tiempo de Ejecución (ms) | Factor $b^*$ | Cantidad de nodos de la solución
|---|---|---|---|---|---|
| A* $h_1$ (Euclidiana) | 20032.24 | 862 | 15.74 | 1.012 | 208
| A* $h_2$ (Haversine) | 20032.24 | 859 | 24.91 | 1.011 | 208
| A* $h_3$ (Personalizada) | 20032.24 | 1153 | 20.22 | 1.014 | 208
| Greedy Best-First | 22675.11 | 437 | 4.04 | 1.005 | 234

Prueba 1500 nodos, 1 empresa, 19 destinos.

Distancia euclidiana(directa) total = 11399.65m

Distancia Haversine(directa) total = 11419.69m

| Algoritmo / Heurística | Distancia en metros | Nodos expandidos | Tiempo de Ejecución (ms) | Factor $b^*$ | Cantidad de nodos de la solución
|---|---|---|---|---|---|
| A* $h_1$ (Euclidiana) | 11563.25 | 918 | 16.46 | 1.020 | 151
| A* $h_2$ (Haversine) | 11563.25 | 918 | 25.68 | 1.020| 151
| A* $h_3$ (Personalizada) | 11563.25 | 1103 | 20.49 | 1.021 | 151
| Greedy Best-First | 12375.67 | 300 | 3.28| 1.008 | 149

Prueba 500 nodos, 1 empresa, 99 destinos.

Distancia euclidiana(directa) total = 22910.13m

Distancia Haversine(directa) total = 22950.40m

| Algoritmo / Heurística | Distancia en metros | Nodos expandidos | Tiempo de Ejecución (ms) | Factor $b^*$ | Cantidad de nodos de la solución
|---|---|---|---|---|---|
| A* $h_1$ (Euclidiana) | 47654.24 | 2242 | 76.64 | 1.004 | 614
| A* $h_2$ (Haversine) | 47654.24 | 2239 | 129.82 | 1.004 | 614
| A* $h_3$ (Personalizada) | 47654.24 | 2760 | 92.88 | 1.004 | 614
| Greedy Best-First | 51020.50 | 1345 | 23.32 | 1.002 | 636

Prueba 1500 nodos, 1 empresa, 299 destinos.

Distancia euclidiana(directa) total = 39960.84m

Distancia Haversine(directa) total = 40031.07m

| Algoritmo / Heurística | Distancia en metros | Nodos expandidos | Tiempo de Ejecución (ms) | Factor $b^*$ | Cantidad de nodos de la solución
|---|---|---|---|---|---|
| A* $h_1$ (Euclidiana) | 105910.76 | 4216 | 287.05 | 1.001 | 1407
| A* $h_2$ (Haversine) | 105910.76 | 4206 | 618.48 | 1.001 | 1407
| A* $h_3$ (Personalizada) | 101855.31 | 4888 | 354.17 | 1.002 | 1345
| Greedy Best-First | 109594.14 | 2713 | 143.68 | 1.001 | 1438

### 4.2 Factor de Ramificación Efectiva ($b^*$)

El factor de ramificación efectiva mide la eficiencia de una función heurística. Se define como el número equivalente de hijos por nodo en un árbol uniforme de profundidad $d$ para explorar $N$ nodos totales:

$$N + 1 = 1 + b^* + (b^*)^2 + \dots + (b^*)^d = \frac{(b^*)^{d+1} - 1}{b^* - 1}$$

Un valor de $b^*$ cercano a 1.0 indica una heurística altamente informada que guía la búsqueda casi en línea recta hacia la meta con mínima exploración infructuosa.

En las pruebas el algoritmo de Greedy Best-First la mayor parte de las veces tuvo un factor b* más cercano a 1.00 que las heuristicas A*, sin embargo la solución entregada no es la más optima.

Como se predijo en el análisis de admisibilidad existen casos en los que nuestra heurística ponderada falla(especificamente en nuestro test con 1500 nodos, 1 empresa y 299 destino) y empieza a entregar datos que ya no tienen sentido a pesar de imprimir la misma solución.

De los datos observados de la prueba de tests se puede decir que el algoritmo más balanceado es la heuristica con distancias euclidianas, dado que entrega el camino más optimo, dentro de las heuristicas A* es la que menos tiempo tarda en ejecutarse, y entre mas nodos tengan los grafos es mas optimo su b* en algunos casos siendo igual al que tiene Greedy Best-First.

## 5. Cuestionario y Análisis de Resultados

**1. ¿Por qué $h_2$ (Haversine) es más precisa que $h_1$ (Euclidiana) para coordenadas geográficas?**

Es más precisa por el echo de que tiene los costos reales(distancias en metros) de las calles con respecto a la curvatura de la tierra, por ende al momento de recalcular las distancias una vez que avanzamos por los nodos, vamos a elegir el que tenga el mejor costo de una manera mas realista lo que en ocasiones puede alterar los nodos expandidos.

**2. Construye un ejemplo concreto donde Greedy falla en el mapa descargado.**

*Escenario de falla:* Supongamos una configuración en forma de "calle sin salida" o una barrera geográfica (un río, una vía de tren o una manzana muy larga) ubicada entre el origen $S$ y el destino $T$.
- *Comportamiento de GBFS:* GBFS evalúa únicamente $h(n)$. Ante una bifurcación, elegirá sistemáticamente la calle que se dirija frontalmente hacia $T$, ingresando hasta el fondo de una calle sin salida o bordeando la barrera por el tramo más largo simplemente porque los nodos intermedios están físicamente más cerca de $T$.
- *Comportamiento de A\*:* Al incluir $g(n)$, A* detecta que el costo acumulado por adentrarse en la vía muerta o rodear la barrera incrementa el costo total $f(n)$, por lo que aborta ese camino y explora una vía alternativa más larga visualmente, pero óptima en distancia real acumulada.

**3. ¿Qué ocurre si se multiplica $h$ por una constante $k > 1$ (heurística inflada)? ¿Sigue siendo admisible?**

Si tomamos $h'(n) = k \cdot h(n)$ con $k > 1$:

- *Admisibilidad:* Se pierde la admisibilidad. Si para algún nodo el costo estimado $h(n)$ era igual o cercano al costo real óptimo $h^*(n)$, al multiplicarlo por $k > 1$ se obtiene $h'(n) > h^*(n)$, violando la condición $h'(n) \le h^*(n)$.
- *Optimalidad:* A* pierde la garantía de encontrar el camino más corto o de menor costo.
- *Efecto práctico (Weighted A\*):* A pesar de perder la optimalidad estricta, la búsqueda se vuelve mucho más "agresiva" o enfocada hacia la meta, reduciendo considerablemente los nodos expandidos y el tiempo de cómputo. El costo de la ruta resultante estará acotado por un factor superior máximo de $k \cdot C^*$.

## 6. Conclusiones

- **Eficiencia en la búsqueda:** La incorporación de una heurística geográfica en A* reduce el espacio de búsqueda explorado en comparación con Greedy Best-First sin perder la calidad ni la optimalidad del camino encontrado.
- **Selección de heurísticas:** Para análisis sobre mapas en coordenadas geográficas (Lat/Lon), la distancia de Haversine ($h_2$) ofrece la estimación de menor distorsión y garantiza admisibilidad y consistencia estrictas.
- **Compromiso velocidad-optimalidad:** Greedy Best-First Search expande notablemente menos nodos y ejecuta más rápido, pero no garantiza obtener la solución más optima.

## 7. Referencias

https://www.ecured.cu/Algoritmo_de_Búsqueda_Heurística_A*    -->  Algoritmo de busqueda heuristica A*
https://www.datacamp.com/es/tutorial/a-star-algorithm        -->  Algoritmo A*
https://osmnx.readthedocs.io/en/stable/user-reference.html   -->  Documentación OSMNX
https://networkx.org/documentation/stable/tutorial.html#attributes  --> Documentacion NetWorkX
https://docs.python.org/es/3/library/heapq.html    --> Documentación Python
https://docs.pytest.org/en/stable/     --> Documentación Pytest