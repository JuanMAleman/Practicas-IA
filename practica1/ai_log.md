# Registro de Uso de IA

En este documento se registra el uso de IA como apoyo para la 
realización ciertas secciones de la práctica 1.

## Herramienta(s) utilizada(s)

- **Nombre: Gemini, Copilot**
- **Versión / Modelo: 3.6 Flash Gemini**
- **Enlace: https://google.com, https://microsoft.com**

---

## Registro de Interacciones

búsqueda informada grafos

**Prompt utilizado:**

```
La búsqueda informada (o heurística) en grafos es una técnica de inteligencia artificial que utiliza conocimiento específico del problema y funciones de evaluación para guiar la exploración hacia la meta de manera más eficiente que los métodos ciegos.
Conceptos Clave
• Función Heurística h(n): Estima el costo del camino más barato desde el nodo actual n hasta el nodo objetivo.
• Admisibilidad: Una heurística es admisible si nunca sobreestima el costo real para llegar a la meta.
• Cola de prioridad: Estructura de datos usada para ordenar los estados según su valor prometedor o costo estimado.
Algoritmos Principales
• Búsqueda Voraz (Greedy Best-First Search): Expande el nodo que parece estar más cerca de la meta según h(n). Es rápida, pero no garantiza encontrar el camino óptimo.
• A* Search: Combina el costo real acumulado g(n) y la heurística h(n) mediante la función f(n) = g(n) + h(n). Es completo y óptimo si la heurística es admisible.
Si deseas profundizar en este tema, dime si quieres que te ayude a:
• Desarrollar un ejemplo práctico paso a paso con el algoritmo A*
• Comparar la complejidad temporal y espacial frente a la búsqueda no informada (BFS/DFS)
• Escribir código en Python para implementar una función heurística en un grafo
```

**Uso que se le dio / Observaciones:**

Simplemente teórico.

---



**Prompt utilizado:**

```
El f(n) con el menor costo es la solucion?
```

**Resultado obtenido:**

```
No directamente. El nodo con el \(f(n)\) de menor costo no es la solución automática, sino el siguiente nodo que el algoritmo decide explorar (expandir). En el algoritmo A*, el valor \(f(n) = g(n) + h(n)\) representa una estimación del costo total del camino completo si pasas por ese nodo. El proceso funciona así: El algoritmo revisa su lista de nodos pendientes (frontera) y selecciona el que tiene el \(f(n)\) más bajo.Extrae ese nodo de la lista y comprueba si es el nodo meta.Si es la meta, entonces sí: se ha encontrado la solución óptima y el algoritmo termina.Si no es la meta, el algoritmo descubre sus nodos vecinos, calcula sus respectivos valores de \(f(n)\) y los añade a la lista para seguir buscando. Por lo tanto, un \(f(n)\) bajo solo significa que vas por muy buen camino, pero la solución real se confirma únicamente cuando el nodo extraído con el menor costo resulta ser el objetivo final. ¿Qué te gustaría analizar ahora para dejar claro este concepto?Ver un ejemplo numérico corto de cómo cambia \(f(n)\) paso a paso.Entender qué pasa si la heurística \(h(n)\) falla o sobreestima el costo.Ver el pseudocódigo de cómo la cola de prioridad maneja este menor costo.Dime el número de tu preferencia para continuar.
```

**Uso que se le dio / Observaciones:**

F(n) es el nodo de menor costo que el algoritmo decide explorar, al final cuando haya explorado todos los nodos de menor costo y llegue al último nodo destino suma los costos de cada una de las calles(aristas) por las que viajo y ese es el costo total de la solución, de igual forma con estos nodos y aristas se va a armar de manera visual la solución en los grafos.

---

**Prompt utilizado:**

```
oye una pregunta en este algortmo se usan latitudes de los puntos para saber que tanto se aleja uno del otro o son los puros costos de la euritica en metro comparandolos?
```

**Resultado obtenido:**

```
¡Es una excelente pregunta! La respuesta corta es que las dos cosas se combinan: se usan las coordenadas (como las latitudes) para calcular matemáticamente los metros de la heurística. Para entenderlo a fondo, el algoritmo en sí mismo no entiende de geografía, mapas o satélites; solo procesa números abstractos. Sin embargo, los ingenieros y programadores usamos la geografía para "alimentar" al algoritmo. Aquí te muestro cómo se conectan ambos conceptos en el mundo real: 1. El costo real acumulado, \(g(n)\) (En metros/kilómetros reales)Es la distancia exacta que ya has recorrido sobre las calles o carreteras. Si vas en auto de la esquina A a la esquina B, son los metros reales que marca tu odómetro circulando por el asfalto. 2. El costo de la heurística, \(h(n)\) (Donde entran las latitudes)La heurística necesita ser una estimación en línea recta hacia el objetivo (el famoso "como vuela el cuervo"). Para calcular esta línea recta de forma matemática entre dos puntos del planeta, el programador utiliza las latitudes y longitudes de los nodos. Existen fórmulas matemáticas específicas para esto: Fórmula de Haversine: Es la más usada en mapas reales (como Google Maps). Toma la latitud y longitud de dos puntos y, considerando la curvatura de la Tierra, te devuelve la distancia exacta en metros o kilómetros en línea recta.Distancia Euclidiana: Si el mapa es plano o una cuadrícula simple de un videojuego, se usa el teorema de Pitágoras con coordenadas \((x, y)\). En resumen: ¿Cómo se calcula entonces \(f(n)\)?Cuando el algoritmo evalúa un nodo, hace lo siguiente: Mira cuántos metros reales ya caminó por las calles para llegar ahí (\(g(n)\)).Toma la latitud y longitud del nodo actual y la del nodo meta, aplica la fórmula matemática (como Haversine) y obtiene los metros estimados en línea recta (\(h(n)\)).Suma ambos valores en metros: \(f(n) = \text{metros reales} + \text{metros por latitud}\). De esta forma, las latitudes se transforman en metros competitivos que el algoritmo puede comparar directamente para saber qué ramificación se está alejando o acercando a la meta. ¡Con esto ya tienes los cimientos completos de cómo funcionan los sistemas de navegación reales! Para continuar, ¿qué te resultaría más útil ahora?Ver la fórmula matemática en código de cómo la latitud/longitud se convierte en metros para la heurística.Hacer el pequeño test de 2 preguntas para consolidar todo lo que hemos aprendido hoy.Analizar cómo cambia el algoritmo si en vez de optimizar distancia (metros) queremos optimizar tiempo (tráfico/velocidad).Dime el número de tu preferencia para proceder.
```

**Uso que se le dio / Observaciones:**

Cálculo de las distancias euclidianas, haverstine y ponderada usa las latitudes y longitudes de los nodos.

---


**Prompt utilizado:**

```
oye como puedo hacer unos archivos de test(test.py) que al ejecutarlos me modifiquen ciertos valores de otro archivo donde tengo algoritmos que su resultado depende de estos valores
```

**Resultado obtenido:**

```
Para lograr esto, la mejor práctica en programación es modularizar tu código. En lugar de modificar el archivo de texto directamente, debes transformar tu algoritmo en una función que reciba parámetros y llamarla desde tu archivo de pruebas.
Aquí tienes la estructura ideal para hacerlo de forma limpia y automática:
1. Modifica tu archivo de algoritmos (fase2.py)
Transforma tu algoritmo en una función que acepte los valores variables como argumentos de entrada y devuelva el resultado.
python
#Archivo_Algoritmo.py

def ejecutar_algoritmo(valor_a, valor_b):
    # Aquí va tu lógica actual. Este es solo un ejemplo:
    resultado = (valor_a * 2) + valor_b
    return resultado
Usa el código con precaución.
2. Crea tu archivo de pruebas (test.py)
En este archivo importas la función de Archivo_Algoritmo, defines los diferentes escenarios (valores) que quieres probar y los ejecutas en cadena.
python
# test.py
from Archivo_Algoritmo import ejecutar_algoritmo

# Definimos diferentes escenarios de prueba (Valor A, Valor B, Resultado Esperado)
pruebas = [
    {"a": 5,  "b": 10, "esperado": 20},
    {"a": 0,  "b": 3,  "esperado": 3},
    {"a": -2, "b": 5,  "esperado": 1},
]

print("--- Iniciando Pruebas de Algoritmo ---")

for i, caso in enumerate(pruebas, 1):
    # Ejecuta el algoritmo pasándole los valores específicos de este test
    resultado_obtenido = ejecutar_algoritmo(caso["a"], caso["b"])
    
    # Verifica si el resultado es el que esperabas
    if resultado_obtenido == caso["esperado"]:
        print(status := f"Test {i}: PASÓ ✅ (Valores: a={caso['a']}, b={caso['b']} -> Resultado: {resultado_obtenido})")
    else:
        print(status := f"Test {i}: FALLÓ ❌ (Esperaba {caso['esperado']}, pero dio {resultado_obtenido})")
Usa el código con precaución.
🚀 ¿Cómo se ejecuta?
Solo debes abrir tu terminal y correr el archivo de pruebas:
bash
python test.py
Usa el código con precaución.
Al hacerlo, test.py alimentará automáticamente a fase2.py con cada grupo de variables sin necesidad de editar manualmente los archivos.
¿Qué te parece este enfoque? Si lo prefieres, podemos adaptarlo exactamente a tu caso real. Cuéntame:
1. ¿Qué tipo de valores necesitas cambiar? (¿Números, textos, listas, rutas de archivos?)
2. ¿Cómo recibe los datos tu archivo Archivo_Algoritmo actualmente? (¿Están fijos en variables arriba del archivo, o los lee de un TXT/JSON?)
3. ¿Te gustaría ver cómo hacer esto mismo usando una herramienta profesional como pytest?
Dime el número de tu opción o compárteme un pedazo de tu código actual para adaptarlo directamente.

```

**Uso que se le dio / Observaciones:**

Inicialmente, usaba una logica similar para realizar los test, los cuales corrían con python nombretest.py, después se cambió a pytest -v -s

---



**Prompt utilizado:**

```
Con un solo comando como instalo estas librerias?
import osmnx as oximport networkx as nximport matplotlib.pyplot as plt from collections import dequeimport randomimport heapqimport mathimport timeimport sys
```

**Resultado obtenido:**

```
Para instalar todas las librerías externas que necesitas con un solo comando, ejecuta lo siguiente en tu terminal:
bash
pip install osmnx networkx matplotlib
Usa el código con precaución.
🔍 ¿Por qué solo estas tres?
Las demás librerías que aparecen en tus import (collections, random, heapq, math, time y sys) vienen integradas por defecto en Python (Standard Library), por lo que no requieren ninguna instalación adicional.
⚠️ Nota importante sobre OSMnx
La librería OSMnx depende de paquetes geoespaciales complejos (como Shapely o Fiona). Si trabajas en Windows o Mac y el comando anterior te llega a dar algún error de compilación, la forma más limpia y recomendada por sus desarrolladores es instalarla usando Anaconda o Miniconda con este comando único:
bash
conda install -c conda-forge osmnx
Usa el código con precaución.
¿Qué tipo de proyecto estás desarrollando? Si me compartes tu idea, puedo ayudarte a:
1. Configurar el entorno virtual para que no tengas conflictos de dependencias.
2. Escribir la estructura básica del grafo de calles con OSMnx y NetworkX.
3. Crear un algoritmo personalizado (como una búsqueda en anchura o Dijkstra) usando tus import.
Dime el número de la opción que prefieras o descríbeme brevemente tu código para ponernos a trabajar en ello.
```

**Uso que se le dio / Observaciones:**

Preparar el README.md para señalar las instrucciones a seguir para configurar un entorno de ejecución para nuestro código fase2.py y nuestros tests.

---


**Prompt utilizado:**

```
cola de prioridad estructura de datos
```

**Resultado obtenido:**

```
Una cola de prioridad es un tipo de dato abstracto similar a una cola convencional, pero con la diferencia de que cada elemento tiene una prioridad asignada. En lugar de seguir estrictamente el principio FIFO (First In, First Out / Primero en entrar, primero en salir), los elementos se procesan y se extraen según su nivel de prioridad. Si dos elementos comparten exactamente la misma prioridad, se despachan respetando el orden en el que llegaron a la cola. Wikipedia +3⚙️ Operaciones PrincipalesCualquier implementación estándar de una cola de prioridad debe soportar eficientemente las siguientes funciones: YouTube·Ignacio RuedaInsertar (push / add): Agrega un nuevo elemento a la cola junto con su respectivo valor de prioridad.Eliminar el máximo/mínimo (pop / poll): Extrae y remueve de la cola el elemento con la prioridad más alta.Obtener el frente (top / peek): Devuelve el elemento con mayor prioridad sin quitarlo de la estructura. YouTube·Ignacio Rueda +1🛠️ Formas de Implementación y ComplejidadDependiendo de la estructura interna que elijas para programarla, el rendimiento (Notación Big-O) varía de forma considerable: adrianmejia.comEstructura de Datos BaseInserción (push)Extracción (pop)Arreglo o Lista DesordenadaO(1)O(n)Arreglo o Lista OrdenadaO(n)O(1)Montículo Binario (Binary Heap)\(O(\log n)\)\(O(\log n)\)💡 Nota: El Montículo Binario (Heap) es la opción óptima y más utilizada en el software real debido a que equilibra ambas operaciones clave en tiempo logarítmico (\(O(\log n)\)). Puede configurarse como un Max-Heap (el valor más alto sale primero) o un Min-Heap (el valor más pequeño sale primero). GitHub +1🌍 Aplicaciones en el Mundo RealLas colas de prioridad son indispensables para resolver múltiples problemas de computación y sistemas distribuidos: Algoritmos de Grafos: Cruciales para encontrar rutas óptimas, como en el algoritmo de caminos mínimos de Dijkstra o el algoritmo de búsqueda \[A^{*}\]. YouTube·OpenWebinarsSistemas Operativos: Para la planificación de procesos del CPU (donde ciertas tareas del sistema operativo tienen prioridad sobre las aplicaciones de usuario). Compresión de Datos: El algoritmo de codificación de Huffman las utiliza para construir árboles de frecuencia eficientes. Si quieres ver un ejemplo práctico de cómo construir, configurar y manipular este componente en código paso a paso, te sugiero revisar este tutorial: 3mCÓMO CREAR UNA COLA DE PRIORIDAD EN JAVA7.8 k reproducciones · hace 6 añosYouTube · OpenWebinars¿Qué te gustaría hacer a continuación con este concepto? Puedo ayudarte a:Ver un ejemplo de código en un lenguaje específico (como Python, Java, C++ o JavaScript).Entender en profundidad cómo funciona un montículo binario (heap) para organizar los datos internamente.Diseñar un ejercicio interactivo o caso práctico (ej. sistema de atención médica para urgencias).Por favor, escribe el número de tu elección o dime qué necesitas.
```

**Uso que se le dio / Observaciones:**

Conocimiento teórico de la cola de prioridad.

---







**Prompt utilizado:**

```
En python como se usa esa cola de prioridad, y como se aplicaria en un grafo en el que tenemos la caracteristica lenght(metros), para que obtener ese elemento y usarlo
```

**Resultado obtenido:**

```
En Python, la forma más eficiente y nativa de usar una cola de prioridad es mediante el módulo heapq. Cuando trabajas con grafos de OpenStreetMap (usando NetworkX), la característica de distancia se escribe en inglés como length. Para usarla en la cola de prioridad, debes guardar elementos con el formato (prioridad, nodo_id), donde la prioridad será el valor de length. Python ordenará automáticamente la cola de menor a mayor distancia. Aquí tienes el código directo para crear la cola, meter nodos con sus distancias, extraer el más cercano y usar sus datos: pythonimport heapq
import networkx as nx

# 1. Supongamos que 'empresa' es tu grafo de OpenStreetMap (MultiDiGraph)
# Si no tienes uno, creamos uno de prueba para que el código funcione:
empresa = nx.MultiDiGraph()
empresa.add_edge("Nodo_A", "Nodo_B", length=150.5)
empresa.add_edge("Nodo_A", "Nodo_C", length=42.3)
empresa.add_edge("Nodo_B", "Nodo_D", length=89.1)

# =====================================================================
# 2. CREAR E INSERTAR ELEMENTOS EN LA COLA DE PRIORIDAD
# =====================================================================
cola_prioridad = []

# Recorremos las calles (aristas) del grafo para registrar los destinos y sus metros
for origen, destino, datos_calle in empresa.edges(data=True):
    metros = datos_calle.get('length', 0)  # Extraemos el peso 'length'
    
    # Insertamos en la cola con el formato: (prioridad, dato)
    # heapq.heappush guarda todo ordenado automáticamente por el primer elemento (metros)
    heapq.heappush(cola_prioridad, (metros, destino))

print(f"Estado de la cola (desordenada internamente pero eficiente): {cola_prioridad}\n")

# =====================================================================
# 3. EXTRAER Y USAR EL ELEMENTO CON MENOR 'LENGTH' (MÁS CERCANO)
# =====================================================================
# heapq.heappop siempre saca el elemento con el valor de 'length' más pequeño
metros_mas_corto, nodo_elegido = heapq.heappop(cola_prioridad)

print("--- ELEMENTO EXTRAÍDO ---")
print(f"El nodo más cercano es: {nodo_elegido}")
print(f"Distancia recorrida para llegar: {metros_mas_corto} metros")

# =====================================================================
# 4. USAR EL ELEMENTO EXTRAÍDO
# =====================================================================
# Ahora puedes usar 'nodo_elegido' para buscar sus coordenadas o seguir navegando
if nodo_elegido in empresa.nodes:
    print(f"\n¡Listo! Ahora procesando el nodo {nodo_elegido} en el algoritmo...")
    # Aquí iría tu lógica, por ejemplo, revisar las calles que salen de este nodo
Usa el código con precaución.🔍 Puntos clave del código:heapq.heappush(lista, (prioridad, valor)): Introduce el nodo en la cola. Es vital que la distancia (length) sea el primer elemento de la tupla, ya que Python compara las tuplas de izquierda a derecha. heapq.heappop(lista): Extrae y elimina la tupla con el length más pequeño en tiempo \(O(\log n)\). Devuelve la tupla completa, la cual puedes desestructurar directamente en dos variables: metros, nodo = heapq.heappop(...). ¿Qué te gustaría implementar ahora con este código? Puedo ayudarte a:Integrar esta cola en el código completo del algoritmo de Dijkstra para calcular la ruta más corta real.Hacer un bucle while que procese todos los nodos de la cola hasta que quede vacía.Filtrar los nodos para que no se repitan si el grafo tiene calles de doble sentido (nodos visitados).Escribe el número de lo que necesites o dime tu siguiente paso.
```

**Uso que se le dio / Observaciones:**

Este código ayudó a implementar la cola de prioridad en nuestro código python, con el objetivo de que se elijan los caminos con el menor costo, en específico esto lo utilizamos en nuestras funciones AlgoritmoAeuclidiano, AlgoritmoAhaversine, AlgoritmoACombinado y AlgoritmoGreedyEuclidiano.

---



**Prompt utilizado:**

```
Que causa este error: TypeError: 'int' object is not subscriptable
```

**Resultado obtenido:**

```
Este error, TypeError: 'int' object is not subscriptable, significa que intentaste usar corchetes [ ] (para indexar o rebanar) sobre una variable que en realidad contiene un número entero (int). En Python, los números no tienen índices.
En el contexto de tu código con OpenStreetMap y NetworkX, este error ocurre casi siempre por una de estas dos razones:
🚨 Causa 1: Usaste corchetes en un ID de nodo
Si tu variable empresa resultó ser una lista de IDs de nodos (números de OpenStreetMap como 25489115), e intentaste obtener el primer elemento usando dos pares de corchetes o tratándola como una matriz.
• Código que da error:python
nodo = empresa[0][0]  # ¡Error! empresa[0] ya es un entero (el ID), no puedes ponerle otro [0]
Usa el código con precaución.
• Solución: Usa un solo juego de corchetes:python
nodo = empresa[0]
Usa el código con precaución.
🚨 Causa 2: Modificaste el orden al hacer sorted() con los nodos
Cuando creaste el identificador bidireccional para el set, si tu variable u o v ya era un número entero (el ID del nodo), e intentaste acceder a ella con corchetes por accidente dentro de la función.
• Código que da error:python
identificador = tuple(sorted([u[0], v[0]]))  # ¡Error! u y v ya son enteros, no llevan [0]
Usa el código con precaución.
• Solución: Pasa las variables directamente:python
identificador = tuple(sorted([u, v]))
Usa el código con precaución.
Para darte la corrección exacta sin adivinar, ¿podrías compartirme la línea de código específica donde saltó el error?
Pega la línea problemática aquí y te digo exactamente qué corchete debes remover para solucionarlo de inmediato.

```

**Uso que se le dio / Observaciones:**

Solución de errores.

---


**Prompt utilizado:**

```
Como arreglo este error? raise nx.NetworkXError("Frozen graph can't be modified")networkx.exception.NetworkXError: Frozen graph can't be modified
```

**Resultado obtenido:**

```
Este error ocurre porque estás intentando modificar el grafo empresa (añadiendo nodos, borrando aristas o cambiando atributos) después de que OSMnx o NetworkX lo bloquearon en memoria para optimizar el rendimiento. Un grafo "congelado" (frozen) es estrictamente de solo lectura.
La forma más rápida y limpia de solucionarlo es crear una copia mutable (que sí se pueda modificar) del grafo antes de meterlo a tu bucle.
🛠️ La Solución:
Justo después de cargar o recibir tu grafo empresa, añade esta línea para descongelarlo:
python
# Creamos una copia idéntica que SÍ permite modificaciones
empresa = nx.MultiDiGraph(empresa)  # O nx.DiGraph(empresa) según tu caso
Usa el código con precaución.
💡 ¿Por qué sale este error en tu código?
Aunque en los pasos anteriores planeábamos usar un set() externo para registrar las aristas visitadas (lo cual no modifica el grafo y no debería dar este error), es muy probable que en tu código actual estés intentando hacer algo como:
• empresa.remove_edge(u, v) (para borrar las calles por las que ya pasaste).
• empresa.nodes[nodo]['visitado'] = True (para marcar el nodo directamente dentro del grafo).
Al crear la copia con nx.MultiDiGraph(empresa), el grafo se descongela automáticamente y podrás realizar cualquiera de estas operaciones de modificación sin que Python lance el error.
¿En qué línea de tu código estabas intentando modificar el grafo? Si me compartes esa parte, puedo ayudarte a:
1. Ver si es mejor usar la copia mutable (nx.MultiDiGraph).
2. Reescribir esa línea para usar el set() externo y así no tener que modificar el grafo original (lo cual es más eficiente y rápido).
Dime qué opción prefieres o comparte el fragmento para dejarlo listo.
```

## Resumen General del Uso de IA

- **El uso de IA se limitó a información teórica y ciertos códigos muy específicos la mayor parte de las veces la documentación despejo las dudas**