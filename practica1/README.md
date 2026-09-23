# Práctica 1 - Algoritmos de búsqueda

### Ejecutar

```
usage: main.py [-h] [-a ADDRESS] [-d DISTANCE] [-s START_NODE] [-e END_NODE]
               [-n NODES] [-p POPULATION_SIZE] [-gs GENERATIONS]
               [-b BEST_SAMPLE_SIZE] [-m MUTATION_RATE] [-t {test-only,both}]
               [-g]
               run

positional arguments:
  run                   Sección a ejecutar. Sección 1 (S1): Búsqueda a ciegas;
                        Sección 2 (S2): Búsqueda Informada; Sección 3 (S3):
                        Búsqueda local

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
  -n, --nodes NODES     Cantidad de nodos en rango de [4, 15] para la sección
                        3. (por defecto 10)
  -p, --population-size POPULATION_SIZE
                        Cantidad de poblaciones para algoritmo genético. (por
                        defecto 50)
  -gs, --generations GENERATIONS
                        Cantidad de generaciones para algoritmo genético. (por
                        defecto 50)
  -b, --best-sample-size BEST_SAMPLE_SIZE
                        Cantidad de individuos a seleccionar como mejores para
                        algoritmo genético. (por defecto 50)
  -m, --mutation-rate MUTATION_RATE
                        Probabilidad de mutación, rango de [0, 1]. (por
                        defecto 0.5)
  -t, --test {test-only,both}
                        Opción que indica que las pruebas unitarias se deben
                        ejecutar. both: realiza pruebas unitarias y ejecución.
                        test-only: solo realiza las pruebas unitarias
  -g, --show-graph      Bandera para mostrar el grafo utilizado en la
                        ejecución/pruebas
```

**Nota**: Las opciones `--population-size`, `--generations`, 
`--best-sample-size` y `--mutation-rate` solo son validas si se 
ejecuta la sección 3. Para mostrar el menu de ayuda completo debe
utilizarse el comando,

```shell
# De omitirse 's3', se mostrará el menu sin las opciones 
# para el algoritmo genético
python3 main.py s3 -h
```

### Historial de versiones

#### v0.1.0 Implementación de `GeneticAlgorithm`
- Refactorización de `Metrics`

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
