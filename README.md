# Fase 2 — Algoritmos de Búsqueda en Grafos sobre Redes Viales

En esta fase de la práctica se implementa y compara algoritmos de búsqueda en grafos (A* con heurística Euclidiana, Haversine y Combinada vs. Greedy Best-First) sobre redes viales extraídas de OpenStreetMap mediante `osmnx`.

## Requisitos Previos e Instalación

**Windows**

```bash
python -m venv venv
.\venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Librerías**

```bash
pip install osmnx networkx matplotlib shapely
```

## Estructura del Proyecto

```
.
├── cache/
│
├── src/
│   └── fase2.py          # Script principal con los algoritmos y subgrafo
│
├── tests/
│   ├── test1.py          # Prueba individual
│   ├── test2.py          # Prueba individual
│   └── test3.py          # Prueba individual
│
├── ai_log.md              # Reporte de uso de IA (de ser el caso)
│
└── README.md
```

## Ubicarse en la Carpeta Raíz del Proyecto

```bash
cd ruta/a/tu/proyecto
```

## Ejecución del Código

**Script principal**

```bash
python src/fase2.py
```

**Pruebas**

```bash
python tests/test1.py
python tests/test2.py
python tests/test3.py
```