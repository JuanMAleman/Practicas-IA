import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt 
from collections import deque
import random

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

Grafo_principal = HGrafo()

Grafo_Menor = []


def SubGrafo(G_punto, Grafo_Menor):
    limite_nodos = 100
    nodo_inicio = random.choice(list(G_punto))
    Grafo_Menor = []                                # Subgrafo final
    visitados = set([nodo_inicio])                  # Evita donde ya pasó
    cola_expansion = deque([nodo_inicio])           # Controla la expansión uniforme
    
    while cola_expansion and len(Grafo_Menor) < limite_nodos:
        nodo_actual = cola_expansion.popleft()
        Grafo_Menor.append(nodo_actual)
        
        # Aquí es donde usas el comando que mencionaste para extraer vecinos reales de G
        for vecino in G_punto.neighbors(nodo_actual):
            if vecino not in visitados:
                visitados.add(vecino)
                cola_expansion.append(vecino)

    return Grafo_Menor



gdf_nodes, gdf_edges = ox.graph_to_gdfs(Grafo_principal)

SubG_punto = Grafo_principal.subgraph(SubGrafo(Grafo_principal, Grafo_Menor))

nodos_seleccionados = random.sample(list(SubG_punto.nodes()), 20)
empresa = nodos_seleccionados[0]
destinos = nodos_seleccionados[1:]

for nodo in SubG_punto.nodes():
    SubG_punto.nodes[nodo]['tipo'] = 'normal'

SubG_punto.nodes[empresa]['tipo'] = 'empresa'

for d in destinos:
    SubG_punto.nodes[d]['tipo'] = 'destino'

# 1. Crear listas de formato recorriendo los nodos
colores_nodos = []
tamanios_nodos = []

for nodo, datos in SubG_punto.nodes(data=True):
    tipo = datos.get('tipo', 'normal')
    if tipo == 'empresa':
        colores_nodos.append('#0000FF')    # Azul para la Empresa
        tamanios_nodos.append(100)         # Grande
    elif tipo == 'destino':
        colores_nodos.append('#FF0000')    # Rojo para los Destinos
        tamanios_nodos.append(60)          # Mediano
    else:
        colores_nodos.append('#999999')    # Gris para intersecciones normales
        tamanios_nodos.append(15)          # Pequeño

# 2. Dibujar el mapa con OSMnx
fig, ax = ox.plot_graph(
    SubG_punto, 
    node_color=colores_nodos, 
    node_size=80,
    edge_color='#CCCCCC',
    bgcolor='white',
    show=False, 
    close=False
)

# 2. Recorrer cada arista para extraer su 'length' y colocar el texto en el centro
for u, v, k, data in SubG_punto.edges(keys=True, data=True):
    # Obtener el costo en metros (redondeado a 1 decimal)
    distancia = round(data.get('length', 0), 1)
    
    # Coordenadas (x=longitud, y=latitud) de los dos nodos que forman la arista
    x1, y1 = SubG_punto.nodes[u]['x'], SubG_punto.nodes[u]['y']
    x2, y2 = SubG_punto.nodes[v]['x'], SubG_punto.nodes[v]['y']
    
    # Calcular el punto medio de la arista
    x_mid = (x1 + x2) / 2
    y_mid = (y1 + y2) / 2
    
    # Dibujar la etiqueta del costo en metros
    ax.text(
        x_mid, y_mid, 
        f"{distancia}m", 
        fontsize=7, 
        color="Black", 
        ha='center', 
        va='center',
        bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.7) # Fondo blanco semitransparente
    )




##print(gdf_nodes[['y', 'x', 'geometry']].head())

##print(gdf_edges[['name', 'length', 'highway']].head())

print(SubG_punto.number_of_edges())

print(SubG_punto.number_of_nodes())

plt.show()



