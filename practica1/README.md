# Práctica 1 - Algoritmos de búsqueda

### Ejecutar

```
usage: main.py [-h] [-a ADDRESS] [-d DISTANCE] [-s START_NODE] [-e END_NODE]
               [-t {test-only,both}] [-g]
               run

positional arguments:
  run                   Sección a ejecutar. Sección 1 (S1): Búsqueda a ciegas;
                        Sección 2 (S2): Búsqueda Informada; Sección 3 (S3):
                        Búsqueda local [No implementado]

options:
  -h, --help            show this help message and exit
  -a, --address ADDRESS
                        Dirección del punto del cual se descargará el grafo.
                        (por defecto = 'Escuela Superior de Cómputo')
  -d, --distance DISTANCE
                        Distancia a la redonda, en metros, que abarcará el
                        grafo. (por defecto = 1000)
  -s, --start-node START_NODE
                        Identificador del nodo inicial. (por defecto =
                        aleatorio)
  -e, --end-node END_NODE
                        Identificador del nodo final. (por defecto =
                        aleatorio)
  -t, --test {test-only,both}
                        Opción que indica que las pruebas unitarias se deben
                        ejecutar. both: realiza pruebas unitarias y ejecución.
                        test-only: solo realiza las pruebas unitarias
  -g, --show-graph      Bandera para mostrar el grafo utilizado en la
                        ejecución/pruebas
```

### Historial de versiones

#### v0.0.9 Implementación parcial de `GeneticAlgorithm`

#### v0.0.8 Plantilla de fase 3

#### v0.0.7_1 Reporte de la sección 1

#### v0.0.7 Ajustes de ejecución y avance de reporte

#### v0.0.6 Algoritmo genérico "UFSA": Uninformed Search Algorithms
- Agregados parámetros de nodo de inicio y nodo final

#### v0.0.5 Algoritmo genérico "FS"

#### v0.0.4 Algoritmo BFS

#### v0.0.3 Plantilla de la fase 2

#### v0.0.2 Plantilla completa de la fase 1

#### v0.0.1 Proyecto inicial
