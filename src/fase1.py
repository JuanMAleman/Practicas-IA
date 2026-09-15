import osmnx as ox
import matplotlib.pyplot as plt

place_name = "Gustavo A. Madero, Ciudad de mexico, Mexico"
G_place = ox.graph_from_place(place_name, network_type="drive")
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G_place)

ox.plot_graph(G_place)

print(gdf_nodes[['x', 'y']].head())

print(gdf_edges[['length', 'name', 'maxspeed']].head())