import matplotlib.pyplot as plt
import networkx as nx


def draw_graph(g: nx.Graph):
    # https://networkx.org/documentation/stable/auto_examples/drawing/plot_weighted_graph.html
    # https://matplotlib.org/stable/gallery/shapes_and_collections/fancybox_demo.html

    pos = nx.spring_layout(g, seed=5)
    nx.draw_networkx_nodes(g, pos, node_size=2500, node_color="#E3E8EF", linewidths=2, edgecolors="#97A2B6")

    nx.draw_networkx_edges(g, pos, width=3, edge_color="#CDD5E0")
    nx.draw_networkx_labels(g, pos, font_size=10, font_weight=700)
    edge_labels = nx.get_edge_attributes(g, "length")
    nx.draw_networkx_edge_labels(g, pos, edge_labels, bbox={"boxstyle": "round,pad=0.3", "fc": "#FFF"})

    ax = plt.gca()
    ax.margins(0.05)
    plt.axis("off")
    plt.tight_layout()
    plt.show()
