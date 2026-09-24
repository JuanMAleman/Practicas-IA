import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import logging
import random
import heapq
import math
import time

# ox.settings.overpass_url = "https://overpass.kumi.systems/api/interpreter"


# Grafo con centro en Mercado Soledad, Centro, Guerrero, Cuauhtémoc, 06000 Ciudad de México, CDMX y radio de 3500
# metros que comprende las siguientes alcaldías (Cuauhtémoc, Gustavo A. Madero, Venustiano Carranza y Azcapotzalco)
def h_grafo():
    lat_centro = 19.450
    lon_centro = -99.140
    radio_metros = 3500

    g_punto = ox.graph_from_point(
        (lat_centro, lon_centro),
        dist=radio_metros,
        network_type="drive"
    )
    return g_punto


def medir_ejecucion(funcion_algoritmo, *args):
    inicio = time.perf_counter()
    p_directo, p_real, nodos_exp, profundidad = funcion_algoritmo(*args)
    fin = time.perf_counter()

    tiempo_ms = (fin - inicio) * 1000  # Convertir segundos a milisegundos
    b_estrella = calcular_b_estrella(nodos_exp, profundidad)
    return p_directo, p_real, nodos_exp, tiempo_ms, b_estrella, profundidad


def distancia_euclidiana(y1, x1, y2, x2):
    # Conversion a metros
    lat_media_rad = math.radians((y1 + y2) / 2)
    dx = (x2 - x1) * 111000 * math.cos(lat_media_rad)
    dy = (y2 - y1) * 111000
    return math.sqrt(dx ** 2 + dy ** 2)


def calcular_b_estrella(n, d, tol=1e-5, max_iter=100):
    """
    Calcula el factor de ramificación efectivo b* de forma numéricamente estable.
    N: Nodos explorados
    d: Profundidad de la solución
    """
    # Casos límite
    if d <= 0 or n <= 0:
        return 0.0
    if n <= d:
        return 1.0

    low = 1.0
    high = float(n)  # El valor de b* jamás superará N

    for _ in range(max_iter):
        mid = (low + high) / 2.0

        # Evitar división por cero cerca de mid = 1
        if abs(mid - 1.0) < 1e-9:
            val = d + 1
        else:
            try:
                # Si mid^(d+1) es muy grande, calculamos usando logaritmos o capturamos la excepción
                log_val = (d + 1) * math.log(mid)
                if log_val > 700:  # e^700 está cerca del límite float
                    val = float('inf')
                else:
                    val = (math.pow(mid, d + 1) - 1.0) / (mid - 1.0)
            except OverflowError:
                val = float('inf')

        if abs(val - (n + 1)) < tol:
            return mid

        if val > (n + 1):
            high = mid
        else:
            low = mid

    return (low + high) / 2.0


def sub_grafo(g_punto, limite_nodos):
    nodo_inicio = random.choice(list(g_punto))
    grafo_menor = []  # Sub grafo final
    # visitados = set([nodo_inicio])  # Evita los nodos donde ya pasó
    visitados = {nodo_inicio}  # Evita los nodos donde ya pasó
    cola_expansion = deque([nodo_inicio])  # Controla la expansión uniforme

    while cola_expansion and len(grafo_menor) < limite_nodos:
        nodo_actual = cola_expansion.popleft()
        grafo_menor.append(nodo_actual)

        for vecino in g_punto.neighbors(nodo_actual):
            if vecino not in visitados:
                visitados.add(vecino)
                cola_expansion.append(vecino)

    return grafo_menor


def algoritmo_aeuclidiano(sub_g_punto, empresa, destinos):
    nodo_actual = empresa
    visitados = {empresa}  # Evita nodos con multiples aristas

    peso_aristas_directas = 0
    peso_aristas_directas2 = 0

    nodos_expandidos = 0
    profundidad_total = 0

    # Lista con todos los destinos a visitar
    pendientes = set(destinos) - {empresa}

    while pendientes:
        x1, y1 = sub_g_punto.nodes[nodo_actual]['x'], sub_g_punto.nodes[nodo_actual]['y']

        cola_paso = []

        # Distancia a los destinos que AÚN NO tienen arista
        for nodo_destino in pendientes:
            x2, y2 = sub_g_punto.nodes[nodo_destino]['x'], sub_g_punto.nodes[nodo_destino]['y']
            da_nodos = distancia_euclidiana(y1, x1, y2, x2)

            heapq.heappush(cola_paso, (da_nodos, nodo_destino))

        # Extraer ÚNICAMENTE el destino objetivo más cercano 
        if cola_paso:
            metros_heuristica, nodo_objetivo = heapq.heappop(cola_paso)

            peso_aristas_directas += metros_heuristica
            # ------------------------------------------------------------
            # EJECUCIÓN DE A* SOBRE NODOS NORMALES HACIA EL NODO OBJETIVO
            # ------------------------------------------------------------

            # Coordenadas de la meta para calcular la heuristica h(n)
            x_meta = sub_g_punto.nodes[nodo_objetivo]['x']
            y_meta = sub_g_punto.nodes[nodo_objetivo]['y']

            # Estrategia de A*: (f_costo, g_costo, nodo_actual_a_star)
            open_set = []

            # Distancia euclidiana inicial h(origen)
            h_inicio = distancia_euclidiana(y1, x1, y_meta, x_meta)
            heapq.heappush(open_set, (h_inicio, 0, nodo_actual))

            # Diccionarios de seguimiento
            g_score = {nodo: float('inf') for nodo in sub_g_punto.nodes()}
            g_score[nodo_actual] = 0

            padres = {}
            camino_encontrado = False

            while open_set:
                f_curr, g_curr, actual_a = heapq.heappop(open_set)

                nodos_expandidos += 1

                if actual_a == nodo_objetivo:
                    camino_encontrado = True
                    peso_aristas_directas2 += g_curr
                    break

                if g_curr > g_score[actual_a]:
                    continue

                for vecino in sub_g_punto.neighbors(actual_a):
                    # Obtener costo de la arista física (longitud de la calle)
                    datos_arista = sub_g_punto.get_edge_data(actual_a, vecino)
                    if datos_arista is None:
                        continue

                    costo_calle = datos_arista[0].get('length', 1)
                    tentative_g = g_score[actual_a] + costo_calle

                    if tentative_g < g_score[vecino]:
                        g_score[vecino] = tentative_g
                        padres[vecino] = actual_a

                        # Heurística euclidiana desde el vecino a la meta: h(n)
                        x_v = sub_g_punto.nodes[vecino]['x']
                        y_v = sub_g_punto.nodes[vecino]['y']
                        h_vecino = distancia_euclidiana(y_v, x_v, y_meta, x_meta)

                        f_vecino = tentative_g + h_vecino
                        heapq.heappush(open_set, (f_vecino, tentative_g, vecino))

            # -----------------------------------------------
            # RECONSTRUCCIÓN DEL CAMINO Y MARCADO DE ARISTAS
            # -----------------------------------------------
            if camino_encontrado:
                curr = nodo_objetivo
                while curr in padres:
                    profundidad_total += 1
                    p = padres[curr]
                    # Identificador='euclidiana', aristas camino real
                    datos_edge = sub_g_punto.get_edge_data(p, curr)[0]
                    datos_edge['tipo'] = "euclidiana"
                    curr = p

            # Actualizar estados
            visitados.add(nodo_objetivo)
            pendientes.remove(nodo_objetivo)
            nodo_actual = nodo_objetivo
    return peso_aristas_directas, peso_aristas_directas2, nodos_expandidos, profundidad_total


def algoritmo_ahaversine(sub_g_punto, empresa, destinos):
    nodo_actual = empresa
    visitados = {empresa}  # Evita nodos con multiples aristas

    peso_aristas_directas = 0
    peso_aristas_directas2 = 0

    nodos_expandidos = 0
    profundidad_total = 0

    # Lista con todos los destinos a visitar
    pendientes = set(destinos) - {empresa}

    while pendientes:
        x1, y1 = sub_g_punto.nodes[nodo_actual]['x'], sub_g_punto.nodes[nodo_actual]['y']

        cola_paso = []

        # Distancia a los destinos que AÚN NO tienen arista
        for nodo_destino in pendientes:
            x2, y2 = sub_g_punto.nodes[nodo_destino]['x'], sub_g_punto.nodes[nodo_destino]['y']

            # Distancia haversine calculada en metros del nodo actual al destino
            da_nodos = ox.distance.great_circle(y1, x1, y2, x2)

            heapq.heappush(cola_paso, (da_nodos, nodo_destino))

        # Extraer ÚNICAMENTE el destino objetivo más cercano 
        if cola_paso:
            metros_heuristica, nodo_objetivo = heapq.heappop(cola_paso)

            peso_aristas_directas += metros_heuristica
            # ------------------------------------------------------------
            # EJECUCIÓN DE A* SOBRE NODOS NORMALES HACIA EL NODO OBJETIVO
            # ------------------------------------------------------------

            # Coordenadas de la meta para calcular la heuristica h(n)
            x_meta = sub_g_punto.nodes[nodo_objetivo]['x']
            y_meta = sub_g_punto.nodes[nodo_objetivo]['y']

            # Estrategia de A*: (f_costo, g_costo, nodo_actual_a_star)
            open_set = []

            # Distancia haversine inicial h(origen)
            h_inicio = ox.distance.great_circle(y1, x1, y_meta, x_meta)
            heapq.heappush(open_set, (h_inicio, 0, nodo_actual))

            # Diccionarios de seguimiento
            g_score = {nodo: float('inf') for nodo in sub_g_punto.nodes()}
            g_score[nodo_actual] = 0

            padres = {}
            camino_encontrado = False

            while open_set:
                f_curr, g_curr, actual_a = heapq.heappop(open_set)

                nodos_expandidos += 1

                if actual_a == nodo_objetivo:
                    camino_encontrado = True
                    peso_aristas_directas2 += g_curr
                    break

                if g_curr > g_score[actual_a]:
                    continue

                for vecino in sub_g_punto.neighbors(actual_a):
                    # Obtener costo de la arista física (longitud de la calle)
                    datos_arista = sub_g_punto.get_edge_data(actual_a, vecino)
                    if datos_arista is None:
                        continue

                    costo_calle = datos_arista[0].get('length', 1)
                    tentative_g = g_score[actual_a] + costo_calle

                    if tentative_g < g_score[vecino]:
                        g_score[vecino] = tentative_g
                        padres[vecino] = actual_a

                        # Heurística haversine desde el vecino a la meta: h(n)
                        x_v = sub_g_punto.nodes[vecino]['x']
                        y_v = sub_g_punto.nodes[vecino]['y']
                        h_vecino = ox.distance.great_circle(y_v, x_v, y_meta, x_meta)

                        f_vecino = tentative_g + h_vecino
                        heapq.heappush(open_set, (f_vecino, tentative_g, vecino))

            # -----------------------------------------------
            # RECONSTRUCCIÓN DEL CAMINO Y MARCADO DE ARISTAS
            # -----------------------------------------------
            if camino_encontrado:
                curr = nodo_objetivo
                while curr in padres:
                    profundidad_total += 1
                    p = padres[curr]
                    datos_edge = sub_g_punto.get_edge_data(p, curr)[0]
                    datos_edge['tipo'] = "haversine"
                    curr = p

            # Actualizar estados
            visitados.add(nodo_objetivo)
            pendientes.remove(nodo_objetivo)
            nodo_actual = nodo_objetivo
    return peso_aristas_directas, peso_aristas_directas2, nodos_expandidos, profundidad_total


def heuristica_combinada(y1, x1, y2, x2, alpha=0.8, costo_giro=15):
    # Distancia euclidiana en metros
    h_dist = distancia_euclidiana(y1, x1, y2, x2)

    # Estimación de giros simples basados en desviación de ejes
    lat_media_rad = math.radians((y1 + y2) / 2)
    dx = abs((x2 - x1) * 111000 * math.cos(lat_media_rad))
    dy = abs((y2 - y1) * 111000)
    giros_estimados = 1 if (dx > 20 and dy > 20) else 0

    # Combinación ponderada
    return alpha * h_dist + (1 - alpha) * (giros_estimados * costo_giro)


def algoritmo_a_combinado(sub_g_punto, empresa, destinos):
    nodo_actual = empresa
    visitados = {empresa}
    peso_aristas_directas = 0
    peso_aristas_directas2 = 0
    pendientes = set(destinos) - {empresa}

    nodos_expandidos = 0
    profundidad_total = 0

    while pendientes:
        x1, y1 = sub_g_punto.nodes[nodo_actual]['x'], sub_g_punto.nodes[nodo_actual]['y']
        cola_paso = []

        for nodo_destino in pendientes:
            x2, y2 = sub_g_punto.nodes[nodo_destino]['x'], sub_g_punto.nodes[nodo_destino]['y']
            da_nodos = heuristica_combinada(y1, x1, y2, x2)
            heapq.heappush(cola_paso, (da_nodos, nodo_destino))

        if cola_paso:
            metros_heuristica, nodo_objetivo = heapq.heappop(cola_paso)
            peso_aristas_directas += metros_heuristica

            x_meta = sub_g_punto.nodes[nodo_objetivo]['x']
            y_meta = sub_g_punto.nodes[nodo_objetivo]['y']

            open_set = []
            h_inicio = heuristica_combinada(y1, x1, y_meta, x_meta)
            heapq.heappush(open_set, (h_inicio, 0, nodo_actual))

            g_score = {nodo: float('inf') for nodo in sub_g_punto.nodes()}
            g_score[nodo_actual] = 0
            padres = {}
            camino_encontrado = False

            while open_set:
                f_curr, g_curr, actual_a = heapq.heappop(open_set)

                nodos_expandidos += 1

                if actual_a == nodo_objetivo:
                    camino_encontrado = True
                    peso_aristas_directas2 += g_curr
                    break

                if g_curr > g_score[actual_a]:
                    continue

                for vecino in sub_g_punto.neighbors(actual_a):
                    datos_arista = sub_g_punto.get_edge_data(actual_a, vecino)
                    if datos_arista is None:
                        continue

                    costo_calle = datos_arista[0].get('length', 1)
                    tentative_g = g_score[actual_a] + costo_calle

                    if tentative_g < g_score[vecino]:
                        g_score[vecino] = tentative_g
                        padres[vecino] = actual_a

                        x_v = sub_g_punto.nodes[vecino]['x']
                        y_v = sub_g_punto.nodes[vecino]['y']
                        h_vecino = heuristica_combinada(y_v, x_v, y_meta, x_meta)

                        f_vecino = tentative_g + h_vecino
                        heapq.heappush(open_set, (f_vecino, tentative_g, vecino))

            if camino_encontrado:
                curr = nodo_objetivo
                while curr in padres:
                    profundidad_total += 1
                    p = padres[curr]
                    datos_edge = sub_g_punto.get_edge_data(p, curr)[0]
                    datos_edge['tipo'] = "combinada"
                    curr = p

            visitados.add(nodo_objetivo)
            pendientes.remove(nodo_objetivo)
            nodo_actual = nodo_objetivo

    return peso_aristas_directas, peso_aristas_directas2, nodos_expandidos, profundidad_total


# ---------------------------
# Función Greedy Best-First (solo h, sin g)
# ---------------------------
def algoritmo_greedy_euclidiano(sub_g_punto, empresa, destinos):
    nodo_actual = empresa
    visitados = {empresa}

    peso_aristas_directas = 0
    peso_aristas_directas2 = 0

    nodos_expandidos = 0
    profundidad_total = 0

    pendientes = set(destinos) - {empresa}

    while pendientes:
        x1, y1 = sub_g_punto.nodes[nodo_actual]['x'], sub_g_punto.nodes[nodo_actual]['y']

        cola_paso = []
        for nodo_destino in pendientes:
            x2, y2 = sub_g_punto.nodes[nodo_destino]['x'], sub_g_punto.nodes[nodo_destino]['y']
            da_nodos = distancia_euclidiana(y1, x1, y2, x2)
            heapq.heappush(cola_paso, (da_nodos, nodo_destino))

        if cola_paso:
            metros_heuristica, nodo_objetivo = heapq.heappop(cola_paso)
            peso_aristas_directas += metros_heuristica

            x_meta = sub_g_punto.nodes[nodo_objetivo]['x']
            y_meta = sub_g_punto.nodes[nodo_objetivo]['y']

            open_set = []

            h_inicio = distancia_euclidiana(y1, x1, y_meta, x_meta)
            heapq.heappush(open_set, (h_inicio, 0, nodo_actual))

            visitados_greedy = {nodo_actual}
            padres = {}
            camino_encontrado = False

            while open_set:
                h_curr, g_curr, actual_a = heapq.heappop(open_set)

                nodos_expandidos += 1

                if actual_a == nodo_objetivo:
                    camino_encontrado = True
                    peso_aristas_directas2 += g_curr
                    break

                for vecino in sub_g_punto.neighbors(actual_a):
                    if vecino not in visitados_greedy:
                        visitados_greedy.add(vecino)
                        padres[vecino] = actual_a

                        datos_arista = sub_g_punto.get_edge_data(actual_a, vecino)
                        costo_calle = datos_arista[0].get('length', 1) if datos_arista else 1
                        g_vecino = g_curr + costo_calle

                        # Solo h(n) para ordenar en Greedy Best-First
                        x_v = sub_g_punto.nodes[vecino]['x']
                        y_v = sub_g_punto.nodes[vecino]['y']
                        h_vecino = distancia_euclidiana(y_v, x_v, y_meta, x_meta)

                        heapq.heappush(open_set, (h_vecino, g_vecino, vecino))

            if camino_encontrado:
                curr = nodo_objetivo
                while curr in padres:
                    profundidad_total += 1
                    p = padres[curr]
                    datos_edge = sub_g_punto.get_edge_data(p, curr)[0]
                    datos_edge['tipo'] = "greedy"
                    curr = p

            visitados.add(nodo_objetivo)
            pendientes.remove(nodo_objetivo)
            nodo_actual = nodo_objetivo

    return peso_aristas_directas, peso_aristas_directas2, nodos_expandidos, profundidad_total


Grafo_Menor = []
gdf_nodes, gdf_edges = None, None


def run(**kwargs):
    global Grafo_Menor, gdf_nodes, gdf_edges
    grafo_principal = h_grafo()

    limite_nodos = kwargs["nodes"]  # int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    num_destinos = kwargs["dst_amount"]  # int(sys.argv[2]) if len(sys.argv) > 2 else 20

    Grafo_Menor = []

    gdf_nodes, gdf_edges = ox.graph_to_gdfs(grafo_principal)

    sub_g_punto = grafo_principal.subgraph(sub_grafo(grafo_principal, limite_nodos)).copy()
    sub_g_punto = nx.MultiDiGraph(sub_g_punto)

    sub_g_haversine = sub_g_punto.copy()

    # Copia limpia para el subgrafo de Greedy
    sub_g_greedy = sub_g_punto.copy()

    sub_g_combinada = sub_g_punto.copy()

    # Formato de los nodos
    nodos_seleccionados = random.sample(list(sub_g_punto.nodes()), num_destinos)
    empresa = nodos_seleccionados[0]
    destinos = nodos_seleccionados[1:]

    for nodo in sub_g_punto.nodes():
        sub_g_punto.nodes[nodo]['tipo'] = 'normal'
        sub_g_greedy.nodes[nodo]['tipo'] = 'normal'
        sub_g_haversine.nodes[nodo]['tipo'] = 'normal'
        sub_g_combinada.nodes[nodo]['tipo'] = 'normal'

    sub_g_punto.nodes[empresa]['tipo'] = 'empresa'
    sub_g_greedy.nodes[empresa]['tipo'] = 'empresa'
    sub_g_haversine.nodes[empresa]['tipo'] = 'empresa'
    sub_g_combinada.nodes[empresa]['tipo'] = 'empresa'

    for d in destinos:
        sub_g_punto.nodes[d]['tipo'] = 'destino'
        sub_g_greedy.nodes[d]['tipo'] = 'destino'
        sub_g_haversine.nodes[d]['tipo'] = 'destino'
        sub_g_combinada.nodes[d]['tipo'] = 'destino'

    colores_nodos = []
    tamanios_nodos = []

    for nodo, datos in sub_g_punto.nodes(data=True):
        tipo = datos.get('tipo', 'normal')
        if tipo == 'empresa':
            colores_nodos.append('#0000FF')  # Azul para nodo empresa
            tamanios_nodos.append(60)  # Grande
        elif tipo == 'destino':
            colores_nodos.append('#FF0000')  # Rojo para nodos destino
            tamanios_nodos.append(30)  # Mediano
        else:
            colores_nodos.append('#999999')  # Gris para nodos normales
            tamanios_nodos.append(15)  # Pequeño

    peso_directo_a, peso_real_a, nodos_a, tiempo_a, b_estrella_a, sol_a = medir_ejecucion(algoritmo_aeuclidiano,
                                                                                          sub_g_punto, empresa,
                                                                                          destinos)

    peso_directo_h, peso_real_h, nodos_h, tiempo_h, b_estrella_h, sol_h = medir_ejecucion(algoritmo_ahaversine,
                                                                                          sub_g_haversine, empresa,
                                                                                          destinos)

    peso_directo_c, peso_real_c, nodos_c, tiempo_c, b_estrella_c, sol_c = medir_ejecucion(algoritmo_a_combinado,
                                                                                          sub_g_combinada, empresa,
                                                                                          destinos)

    peso_directo_g, peso_real_g, nodos_g, tiempo_g, b_estrella_g, sol_g = medir_ejecucion(algoritmo_greedy_euclidiano,
                                                                                          sub_g_greedy, empresa,
                                                                                          destinos)

    logging.info(f"Distancia Euclidiana Total: {peso_directo_a:.2f} m\n")
    logging.info(f"Distancia Haversine total(Haversine): {peso_directo_h:.2f} m")

    # Impresión de resultados de la comparación entre algoritmos(A* y Greedy Best-First)
    logging.info("=" * 97)
    logging.info(
        f"{'Algoritmo':<22} | {'Distancia (m)':<13} | {'Nodos Exp.':<10} | {'Tiempo (ms)':<11} | {'b*':<8}"
        f" | {'N. Solución':<11}")
    logging.info("=" * 97)
    logging.info(
        f"{'A* Euclidiana':<22} | {peso_real_a:<13.2f} | {nodos_a:<10} | {tiempo_a:<11.2f} | {b_estrella_a:<8.3f}"
        f" | {sol_a:<11}")
    logging.info(
        f"{'A* Haversine':<22} | {peso_real_h:<13.2f} | {nodos_h:<10} | {tiempo_h:<11.2f} | {b_estrella_h:<8.3f}"
        f" | {sol_h:<11}")
    logging.info(
        f"{'A* Combinada (H3)':<22} | {peso_real_c:<13.2f} | {nodos_c:<10} | {tiempo_c:<11.2f} | {b_estrella_c:<8.3f}"
        f" | {sol_c:<11}")
    logging.info(
        f"{'Greedy Best-First':<22} | {peso_real_g:<13.2f} | {nodos_g:<10} | {tiempo_g:<11.2f} | {b_estrella_g:<8.3f}"
        f" | {sol_g:<11}")
    logging.info("=" * 97)

    colores_aristas_a = []
    for u, v, k, datos in sub_g_punto.edges(keys=True, data=True):
        if datos.get('tipo') == 'euclidiana':
            colores_aristas_a.append('#FF3333')  # Rojo para A*
        else:
            colores_aristas_a.append("#CCCCCC5A")

    colores_aristas_g = []
    for u, v, k, datos in sub_g_greedy.edges(keys=True, data=True):
        if datos.get('tipo') == 'greedy':
            colores_aristas_g.append('#00AA00')  # Verde para Greedy
        else:
            colores_aristas_g.append("#CCCCCC5A")

    colores_aristas_h = []
    for u, v, k, datos in sub_g_haversine.edges(keys=True, data=True):
        if datos.get('tipo') == 'haversine':
            colores_aristas_h.append('#00A2FF')  # Azul para Haversine
        else:
            colores_aristas_h.append("#CCCCCC5A")

    colores_aristas_c = []
    for u, v, k, datos in sub_g_combinada.edges(keys=True, data=True):
        if datos.get('tipo') == 'combinada':
            colores_aristas_c.append('#9900FF')  # Morado para Heurística Combinada
        else:
            colores_aristas_c.append("#CCCCCC5A")

    if "show_graph" not in kwargs or not kwargs["show_graph"]:
        return

    def plot(titulo_1, titulo_2, colores_aristas_1, colores_aristas_2):
        fig1, ax1 = ox.plot_graph(
            sub_g_punto, node_color=colores_nodos, node_size=tamanios_nodos,
            edge_color=colores_aristas_1, bgcolor='white', show=False, close=False
        )
        ax1.set_title(titulo_1, fontsize=14)

        fig2, ax2 = ox.plot_graph(
            sub_g_greedy, node_color=colores_nodos, node_size=tamanios_nodos,
            edge_color=colores_aristas_2, bgcolor='white', show=False, close=False
        )

        ax2.set_title(titulo_2, fontsize=14)

    # Dibuja A* figure 1 y Greedy figure 2
    plot(
        f"A* Euclidiano - Total: {peso_real_a:.1f}m",
        f"Greedy Best-First (No-Óptimo) - Total: {peso_real_g:.1f}m",
        colores_aristas_a, colores_aristas_g
    )

    plot(
        f"A* Haversine - Total: {peso_real_h:.1f}m",
        f"A* Heurística Combinada (Distancia + Giros) - Total: {peso_real_c:.1f}m",
        colores_aristas_h, colores_aristas_c
    )

    # Mostrar ambas figuras simultáneamente
    plt.show()
