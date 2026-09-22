import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt 
from collections import deque
import random
import heapq
import math

ox.settings.overpass_url = "https://overpass.kumi.systems/api/interpreter"

def HGrafo():
    lat_centro = 19.450
    lon_centro = -99.140
    radio_metros = 3500 

    G_punto = ox.graph_from_point(
        (lat_centro, lon_centro), 
        dist=radio_metros, 
        network_type="drive"
    )
    return G_punto



def distancia_euclidiana(y1, x1, y2, x2):
    # Conversion a metros
    lat_media_rad = math.radians((y1 + y2) / 2)
    dx = (x2 - x1) * 111000 * math.cos(lat_media_rad)
    dy = (y2 - y1) * 111000
    return math.sqrt(dx**2 + dy**2)

Grafo_principal = HGrafo()

Grafo_Menor = []

def SubGrafo(G_punto, Grafo_Menor):
    limite_nodos = 1000
    nodo_inicio = random.choice(list(G_punto))
    Grafo_Menor = []                                # Subgrafo final
    visitados = set([nodo_inicio])                  # Evita donde ya pasó
    cola_expansion = deque([nodo_inicio])           # Controla la expansión uniforme
    
    while cola_expansion and len(Grafo_Menor) < limite_nodos:
        nodo_actual = cola_expansion.popleft()
        Grafo_Menor.append(nodo_actual)
        
        # Comando para extraer vecinos reales de G
        for vecino in G_punto.neighbors(nodo_actual):
            if vecino not in visitados:
                visitados.add(vecino)
                cola_expansion.append(vecino)

    return Grafo_Menor

def AlgoritmoAeuclidiano(SubG_punto, empresa, destinos):
    nodo_actual = empresa
    visitados = set([empresa])  # Evita nodos con multiples aristas

    peso_aristasDirectas = 0
    peso_aristasDirectas2 = 0
    
    # Lista con todos los destinos a visitar
    pendientes = set(destinos) - {empresa}

    while pendientes:
        x1, y1 = SubG_punto.nodes[nodo_actual]['x'], SubG_punto.nodes[nodo_actual]['y']
        
        cola_paso = []
        
        # Distancia a los destinos que AÚN NO tienen arista
        for nodo_destino in pendientes:
            x2, y2 = SubG_punto.nodes[nodo_destino]['x'], SubG_punto.nodes[nodo_destino]['y']
            DANodos = distancia_euclidiana(y1, x1, y2, x2)
            
            heapq.heappush(cola_paso, (DANodos, nodo_destino))

        # Extraer ÚNICAMENTE el destino objetivo más cercano 
        if cola_paso:
            metros_heuristica, nodo_objetivo = heapq.heappop(cola_paso)

            peso_aristasDirectas += metros_heuristica
            # ------------------------------------------------------------
            # EJECUCIÓN DE A* SOBRE NODOS NORMALES HACIA EL NODO OBJETIVO
            # ------------------------------------------------------------
            
            # Coordenadas de la meta para calcular la heuristica h(n)
            x_meta = SubG_punto.nodes[nodo_objetivo]['x']
            y_meta = SubG_punto.nodes[nodo_objetivo]['y']

            # Estrategia de A*: (f_costo, g_costo, nodo_actual_a_star)
            open_set = []
            
            # Distancia euclidiana inicial h(origen)
            h_inicio = distancia_euclidiana(y1, x1, y_meta, x_meta)
            heapq.heappush(open_set, (h_inicio, 0, nodo_actual))

            # Diccionarios de seguimiento
            g_score = {nodo: float('inf') for nodo in SubG_punto.nodes()}
            g_score[nodo_actual] = 0

            padres = {}
            camino_encontrado = False

            while open_set:
                f_curr, g_curr, actual_a = heapq.heappop(open_set)

                if actual_a == nodo_objetivo:
                    camino_encontrado = True
                    peso_aristasDirectas2 += g_curr 
                    break

                if g_curr > g_score[actual_a]:
                    continue

                for vecino in SubG_punto.neighbors(actual_a):
                    # Obtener costo de la arista física (longitud de la calle)
                    datos_arista = SubG_punto.get_edge_data(actual_a, vecino)
                    if datos_arista is None:
                        continue
                        
                    costo_calle = datos_arista[0].get('length', 1)
                    tentative_g = g_score[actual_a] + costo_calle

                    if tentative_g < g_score[vecino]:
                        g_score[vecino] = tentative_g
                        padres[vecino] = actual_a
                        
                        # Heurística euclidiana desde el vecino a la meta: h(n)
                        x_v = SubG_punto.nodes[vecino]['x']
                        y_v = SubG_punto.nodes[vecino]['y']
                        h_vecino = distancia_euclidiana(y_v, x_v, y_meta, x_meta)
                        
                        f_vecino = tentative_g + h_vecino
                        heapq.heappush(open_set, (f_vecino, tentative_g, vecino))

            # -----------------------------------------------
            # RECONSTRUCCIÓN DEL CAMINO Y MARCADO DE ARISTAS
            # -----------------------------------------------
            if camino_encontrado:
                curr = nodo_objetivo
                while curr in padres:
                    p = padres[curr]
                    # Identificador='euclidiana', aristas camino real
                    datos_edge = SubG_punto.get_edge_data(p, curr)[0]
                    datos_edge['tipo'] = "euclidiana"
                    curr = p

            # Actualizar estados
            visitados.add(nodo_objetivo)
            pendientes.remove(nodo_objetivo)
            nodo_actual = nodo_objetivo 
    return peso_aristasDirectas, peso_aristasDirectas2


# ---------------------------
# Funcion Greedy Best-First (solo h, sin g)
# ---------------------------
def AlgoritmoGreedyEuclidiano(SubG_punto, empresa, destinos):
    nodo_actual = empresa
    visitados = set([empresa])

    peso_aristasDirectas = 0
    peso_aristasDirectas2 = 0
    
    pendientes = set(destinos) - {empresa}

    while pendientes:
        x1, y1 = SubG_punto.nodes[nodo_actual]['x'], SubG_punto.nodes[nodo_actual]['y']
        
        cola_paso = []
        for nodo_destino in pendientes:
            x2, y2 = SubG_punto.nodes[nodo_destino]['x'], SubG_punto.nodes[nodo_destino]['y']
            DANodos = distancia_euclidiana(y1, x1, y2, x2)
            heapq.heappush(cola_paso, (DANodos, nodo_destino))

        if cola_paso:
            metros_heuristica, nodo_objetivo = heapq.heappop(cola_paso)
            peso_aristasDirectas += metros_heuristica
            
            x_meta = SubG_punto.nodes[nodo_objetivo]['x']
            y_meta = SubG_punto.nodes[nodo_objetivo]['y']

            open_set = []
            
            h_inicio = distancia_euclidiana(y1, x1, y_meta, x_meta)
            heapq.heappush(open_set, (h_inicio, 0, nodo_actual))

            visitados_greedy = set([nodo_actual])
            padres = {}
            camino_encontrado = False

            while open_set:
                h_curr, g_curr, actual_a = heapq.heappop(open_set)

                if actual_a == nodo_objetivo:
                    camino_encontrado = True
                    peso_aristasDirectas2 += g_curr 
                    break

                for vecino in SubG_punto.neighbors(actual_a):
                    if vecino not in visitados_greedy:
                        visitados_greedy.add(vecino)
                        padres[vecino] = actual_a
                        
                        datos_arista = SubG_punto.get_edge_data(actual_a, vecino)
                        costo_calle = datos_arista[0].get('length', 1) if datos_arista else 1
                        g_vecino = g_curr + costo_calle
                        
                        # Solo h(n) para ordenar en Greedy Best-First
                        x_v = SubG_punto.nodes[vecino]['x']
                        y_v = SubG_punto.nodes[vecino]['y']
                        h_vecino = distancia_euclidiana(y_v, x_v, y_meta, x_meta)
                        
                        heapq.heappush(open_set, (h_vecino, g_vecino, vecino))

            if camino_encontrado:
                curr = nodo_objetivo
                while curr in padres:
                    p = padres[curr]
                    datos_edge = SubG_punto.get_edge_data(p, curr)[0]
                    datos_edge['tipo'] = "greedy"
                    curr = p

            visitados.add(nodo_objetivo)
            pendientes.remove(nodo_objetivo)
            nodo_actual = nodo_objetivo 
            
    return peso_aristasDirectas, peso_aristasDirectas2


gdf_nodes, gdf_edges = ox.graph_to_gdfs(Grafo_principal)

SubG_punto = Grafo_principal.subgraph(SubGrafo(Grafo_principal, Grafo_Menor)).copy()
SubG_punto = nx.MultiDiGraph(SubG_punto)

# Copia limpia para el subgrafo de Greedy
SubG_greedy = SubG_punto.copy()

# Formato de los nodos
nodos_seleccionados = random.sample(list(SubG_punto.nodes()), 20)
empresa = nodos_seleccionados[0]
destinos = nodos_seleccionados[1:]

for nodo in SubG_punto.nodes():
    SubG_punto.nodes[nodo]['tipo'] = 'normal'
    SubG_greedy.nodes[nodo]['tipo'] = 'normal'

SubG_punto.nodes[empresa]['tipo'] = 'empresa'
SubG_greedy.nodes[empresa]['tipo'] = 'empresa'

for d in destinos:
    SubG_punto.nodes[d]['tipo'] = 'destino'
    SubG_greedy.nodes[d]['tipo'] = 'destino'

colores_nodos = []
tamanios_nodos = []

for nodo, datos in SubG_punto.nodes(data=True):
    tipo = datos.get('tipo', 'normal')
    if tipo == 'empresa':
        colores_nodos.append('#0000FF')    # Azul para nodo empresa
        tamanios_nodos.append(60)         # Grande
    elif tipo == 'destino':
        colores_nodos.append('#FF0000')    # Rojo para nodos destino
        tamanios_nodos.append(30)          # Mediano
    else:
        colores_nodos.append('#999999')    # Gris para nodos normales
        tamanios_nodos.append(15)          # Pequeño

Peso_Directo_A, Peso_Real_A = AlgoritmoAeuclidiano(SubG_punto, empresa, destinos)

Peso_Directo_G, Peso_Real_G = AlgoritmoGreedyEuclidiano(SubG_greedy, empresa, destinos)

# Impresion de resultados de la comparacion entre algoritmos(A* y Greedy Best-First)
print(f"Distancia Heurística Teórica Total: {Peso_Directo_A:.2f} m\n")
print(f"[Busqueda A*]     -> Distancia total recorrida en calles: {Peso_Real_A:.2f} m")
print(f"[Busqueda Greedy] -> Distancia total recorrida en calles: {Peso_Real_G:.2f} m")
print("-" * 65)


colores_aristas_a = []
for u, v, k, datos in SubG_punto.edges(keys=True, data=True):
    if datos.get('tipo') == 'euclidiana':
        colores_aristas_a.append('#FF3333')  # Rojo para A*
    else:
        colores_aristas_a.append("#CCCCCC5A")


colores_aristas_g = []
for u, v, k, datos in SubG_greedy.edges(keys=True, data=True):
    if datos.get('tipo') == 'greedy':
        colores_aristas_g.append('#00AA00')  # Verde para Greedy
    else:
        colores_aristas_g.append("#CCCCCC5A")


# Dibuja A* figure 1
fig1, ax1 = ox.plot_graph(
    SubG_punto, 
    node_color=colores_nodos, 
    node_size=tamanios_nodos,
    edge_color=colores_aristas_a,
    bgcolor='white',
    show=False, 
    close=False
)
ax1.set_title(f"A* Search (Óptimo) - Total: {Peso_Real_A:.1f}m", fontsize=14)

# Dibuja Greedy figure 2
fig2, ax2 = ox.plot_graph(
    SubG_greedy, 
    node_color=colores_nodos, 
    node_size=tamanios_nodos,
    edge_color=colores_aristas_g,
    bgcolor='white',
    show=False, 
    close=False
)

ax2.set_title(f"Greedy Best-First (No-Óptimo) - Total: {Peso_Real_G:.1f}m", fontsize=14)

# Mostrar ambas figuras simultáneamente
plt.show()