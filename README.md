# Sistema de Optimización de Rutas de Entrega (A* vs Greedy)

En esta fase de la practica se implementa y compara algoritmos de búsqueda en grafos ($A^*$ con heurística Euclidiana, Haversine y Combinada vs. Greedy Best-First) sobre redes viales extraídas de OpenStreetMap mediante `osmnx`.

## Requisitos Previos e Instalación

```
Windows
python -m venv venv
.\venv\Scripts\activate

Linux / macOS:
python3 -m venv venv
source venv/bin/activate

librerias
pip install osmnx networkx matplotlib shapely
```

### Estructura
|
|__ cache/
|    
|
├── src/
│   └── fase2.py          # Script principal con los algoritmos y subgrafo
├── tests/
│   ├── test1.py          # Prueba individual
│   ├── test2.py          # Prueba individual
│   └── test3.py          # Prueba individual
|
|__ai_log.md              # Reporte de uso de IA(de ser el caso).
|
└── README.md

### Ubicarse en la carpeta raíz del proyecto
bash
cd ruta/a/tu/proyecto

### Ejecución del código

Principal
python src/fase2.py

Tests
python tests/test1.py

```