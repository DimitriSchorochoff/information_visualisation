import networkx as nx
from pyvis.network import Network
import pandas as pd
import numpy as np
import community as community_louvain
import seaborn as sns
import matplotlib.colors
from classes import  *


def load_graph_from_csv(filename_nodes, filename_edges):
    df_node = pd.read_csv(filename_nodes, sep='\t')
    df_edge = pd.read_csv(filename_edges, sep='\t', low_memory=False)

    G = nx.Graph()
    G.add_nodes_from(df_node['#BIOGRID ID'])
    G.add_edges_from(zip(df_edge['BioGRID ID Interactor A'], df_edge['BioGRID ID Interactor B']), color='black')
    return G


def draw_graph(nx_graph):
    nt_graph = Network('1080px', '1920px')
    nt_graph.from_nx(nx_graph)
    nt_graph.toggle_physics(False)
    nt_graph.show('nx.html')
    #nt_graph.save_graph('nx.html')


def add_Node(graph, id, label=None, color=None, size=None, neighbourds=None):
    assert isinstance(graph, nx.Graph)
    graph.add_node(id, label=label, size=size, color=color)
    for elem in neighbourds:
        add_Edge(graph, id, elem)


def add_Edge(graph, node1, node2, label=None, color=None, size=None):
    assert isinstance(graph, nx.Graph)
    graph.add_edge(node1, node2, label=label, color=color, size=size)


def change_node_color(graph, node, color):
    assert isinstance(graph, nx.Graph)
    graph.nodes[node]['color'] = color


def change_node_size(graph, node, size):
    assert isinstance(graph, nx.Graph)
    graph.nodes[node]['size'] = size


def change_edge_color(graph, node1, node2, color):
    assert isinstance(graph, nx.Graph)
    graph[node1][node2]['color'] = color


def change_edge_width(graph, node1, node2, width):
    assert isinstance(graph, nx.Graph)
    graph[node1][node2]['width'] = width


def shortest_path(source, dest, graph):
    path = nx.algorithms.shortest_path(graph, source, dest)
    idx=0
    for i in range(len(path)-1):
        change_node_color(graph, path[idx], 'red')
        change_node_size(graph,path[idx],100)
        idx += 1
        change_edge_color(graph, path[i], path[i+1], 'red')
        change_edge_width(graph, path[i], path[i+1], 100)
    change_node_color(graph, path[idx], 'red')
    change_node_size(graph, path[idx], 100)


def minimum_spanning_tree(graph):
    return nx.algorithms.minimum_spanning_tree(graph)


def clustering_coefficient(graph, nodes=None, avg=False):
    if avg:
        return nx.algorithms.average_clustering(graph)
    #nodes can be an int or a list of int
    return nx.algorithms.clustering(graph, nodes=nodes)


def degree_of_node(graph, nodes=None, avg=False):
    if avg:
        return np.mean([i[1] for i in graph.degree()])
    # nodes can be an int or a list of int
    return graph.degree(nodes)


def find_communities(graph):
    communities = community_louvain.best_partition(graph)
    assert isinstance(communities, dict)
    rgb = sns.color_palette(None, len(set(communities.values())))
    palette = [matplotlib.colors.to_hex(col) for col in rgb]
    for node in communities.keys():
        graph.nodes[node]['color'] = palette[communities[node]]


def layouts(graph):
    pass


def betweenness_centrality(graph):
    pass


def filter(graph):
    pass


if __name__ == "__main__":
    graph = load_graph_from_csv('Data/BIOGRID-PROJECT-glioblastoma_project-GENES.projectindex.csv', 'Data/BIOGRID-PROJECT-glioblastoma_project-INTERACTIONS.tab3.csv')
    #shortest_path(107140, 108517, graph)
    #mst = minimum_spanning_tree(graph)
    find_communities(graph)

    #draw_graph(mst)
    draw_graph(graph)

