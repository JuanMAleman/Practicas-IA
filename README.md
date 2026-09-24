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
pip install osmnx networkx matplotlib pytest
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

## Especificaciones del Equipo de Prueba

| Componente         | Detalle                       |
|--------------------|-------------------------------|
| Equipo             | HP Elite X2 1012 G2           |
| Procesador         | Intel core i5 7300U           |
| Memoria RAM        | 8.00 GB LPDDR3-SDRAM 1867 Mhz |
| Almacenamiento     | 238 GB SSD                    |
| Sistema Operativo  | Windows 10 pro 22H2           |
| Tarjeta Gráfica    | Intel HD Graphics 620         |
| Python             | 3.14.7                        |

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
pytest -v -s
```