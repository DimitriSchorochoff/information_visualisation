import networkx as nx
from pyvis.network import Network
import pandas as pd
import numpy as np
import community as community_louvain
import seaborn as sns
import matplotlib.colors
from classes import *

LAYOUT_DEFAULT = Layout("Default", [])
LAYOUT_BARNES = Layout("Barnes Hut", [Layout_parameter_value("Gravity", -100000, -1, -80000, 1000),
                                      Layout_parameter_value("Central gravity", 0, 100, 0.3, 0.1),
                                      Layout_parameter_value("Spring length", 0, 1000, 250, 10),
                                      Layout_parameter_value("Spring strength", 0, 1, 0.001, 0.001),
                                      Layout_parameter_value("Damping", 0, 1, 0.09, 0.01),
                                      Layout_parameter_value("Overlap", 0, 1, 0, 0.1)])
LAYOUT_FORCEATLAS = Layout("Force Atlas 2Based", [Layout_parameter_value("Gravity", -100000, -1, -50, 10),
                                                  Layout_parameter_value("Central gravity", 0, 100, 0.01, 0.01),
                                                  Layout_parameter_value("Spring length", 0, 1000, 100, 10),
                                                  Layout_parameter_value("Spring strength", 0, 1, 0.08, 0.01),
                                                  Layout_parameter_value("Damping", 0, 1, 0.4, 0.1),
                                                  Layout_parameter_value("Overlap", 0, 1, 0, 0.1)])
LAYOUT_REPULSION = Layout("Repulsion", [Layout_parameter_value("Node distance", 0, 10000, 100, 10),
                                        Layout_parameter_value("Central gravity", 0, 100, 0.2, 0.1),
                                        Layout_parameter_value("Spring length", 0, 1000, 200, 10),
                                        Layout_parameter_value("Spring strength", 0, 1, 0.05, 0.01),
                                        Layout_parameter_value("Damping", 0, 1, 0.09, 0.01)])


def load_graph_from_csv(filename_nodes, filename_edges):
    df_node = pd.read_csv(filename_nodes, sep='\t')
    df_edge = pd.read_csv(filename_edges, sep='\t', low_memory=False)

    G = nx.Graph()
    G.add_nodes_from(df_node['#BIOGRID ID'])
    G.add_edges_from(zip(df_edge['BioGRID ID Interactor A'], df_edge['BioGRID ID Interactor B']), color='black')
    return G, df_node, df_edge


def draw_graph(nx_graph, layout=None):
    nt_graph = Network('1080px', '1920px')
    nt_graph.from_nx(nx_graph)  # TODO find a way to avoid computing this line every time

    if layout is None or layout.name == LAYOUT_DEFAULT.name:
        nt_graph.toggle_physics(False)
    elif layout.name == LAYOUT_REPULSION.name:
        nt_graph.show_buttons(filter_=['physics'])
        nt_graph.repulsion()
    elif layout.name == LAYOUT_FORCEATLAS.name:
        nt_graph.force_atlas_2based()
    elif layout.name == LAYOUT_BARNES.name:
        list_param = layout.parameter_lst
        nt_graph.barnes_hut(gravity=list_param[0].start, central_gravity=list_param[1].start,
                            spring_length=list_param[2].start, spring_strength=list_param[3].start,
                            damping=list_param[4].start, overlap=list_param[5].start)
    else:
        raise Exception("Invalid layout error")

    nt_graph.save_graph('nx.html')


def str_tuple_2_tuple(st):
    st = st.replace("(", "")
    st = st.replace(")", "")
    st = st.split(",")
    return int(st[0]), int(st[1])


def add_Node(graph, id, label=None, color=None, size=None, neighbourds=None):
    assert isinstance(graph, nx.Graph)
    graph.add_node(id, label=label, size=size, color=color)
    for elem in neighbourds:
        add_Edge(graph, id, elem)


def remove_Node(graph, id):
    assert isinstance(graph, nx.Graph)
    graph.remove_node(id)


def add_Edge(graph, node1, node2, label=None, color=None, size=None):
    assert isinstance(graph, nx.Graph)
    graph.add_edge(node1, node2, label=label, color=color, size=size)


def remove_Edge(graph, node1, node2):
    assert isinstance(graph, nx.Graph)
    graph.remove_edge(node1, node2)


def change_node_color(graph, node, color):
    assert isinstance(graph, nx.Graph)
    graph.nodes[node]['color'] = color

def change_all_node_color(graph_save, graph_current, color):
    assert isinstance(graph_save, nx.Graph)
    assert isinstance(graph_current, nx.Graph)

    for node in graph_current.nodes:
        graph_save.nodes[node]['color'] = color
        graph_current.nodes[node]['color'] = color


def change_node_size(graph, node, size):
    assert isinstance(graph, nx.Graph)
    graph.nodes[node]['size'] = size

def change_all_node_size(graph_save, graph_current, size):
    assert isinstance(graph_save, nx.Graph)
    assert isinstance(graph_current, nx.Graph)

    for node in graph_current.nodes:
        graph_current.nodes[node]['size'] = size
        graph_save.nodes[node]['size'] = size

def get_node_color(graph, node):
    assert isinstance(graph, nx.Graph)
    return graph.nodes[node]['color']


def get_node_size(graph, node):
    assert isinstance(graph, nx.Graph)
    return graph.nodes[node]['size']


def change_edge_color(graph, node1, node2, color):
    assert isinstance(graph, nx.Graph)
    graph[node1][node2]['color'] = color

def change_all_edge_color(graph_save, graph_current, color):
    assert isinstance(graph_save, nx.Graph)
    assert isinstance(graph_current, nx.Graph)

    for node1, node2 in graph_current.edges:
        graph_current[node1][node2]['color'] = color
        graph_save[node1][node2]['color'] = color


def change_edge_width(graph, node1, node2, width):
    assert isinstance(graph, nx.Graph)
    graph[node1][node2]['width'] = width

def change_all_edge_width(graph_save, graph_current, width):
    assert isinstance(graph_save, nx.Graph)
    assert isinstance(graph_current, nx.Graph)

    for node1, node2 in graph_current.edges:
        graph_current[node1][node2]['width'] = width
        graph_save[node1][node2]['width'] = width

def get_edge_color(graph, node1, node2):
    assert isinstance(graph, nx.Graph)
    return graph[node1][node2]['color']


def get_edge_width(graph, node1, node2):
    assert isinstance(graph, nx.Graph)
    return graph[node1][node2]['width']


def shortest_path(source, target, graph, method='dijkstra'):
    path = nx.algorithms.shortest_path(graph, source=source, target=target, method=method)
    idx = 0
    for i in range(len(path) - 1):
        change_node_color(graph, path[idx], 'red')
        change_node_size(graph, path[idx], 100)
        idx += 1
        change_edge_color(graph, path[i], path[i + 1], 'red')
        change_edge_width(graph, path[i], path[i + 1], 100)
    change_node_color(graph, path[idx], 'red')
    change_node_size(graph, path[idx], 100)


def minimum_spanning_tree(graph):
    return nx.algorithms.minimum_spanning_tree(graph)


def clustering_coefficient(graph, nodes=None, avg=False):
    if avg:
        return nx.algorithms.average_clustering(graph)
    # nodes can be an int or a list of int
    return nx.algorithms.clustering(graph, nodes=nodes)


def degree_of_node(graph, nodes=None, avg=False):
    if avg:
        return np.mean([i[1] for i in graph.degree()])
    # nodes can be an int or a list of int
    return graph.degree(nodes)

"""
def find_communities(graph, partition=None, resolution=1.0, randomize=None, random_state=None):
    communities = community_louvain.best_partition(graph, partition=partition, resolution=resolution, randomize=randomize, random_state=random_state)
    assert isinstance(communities, dict)
    rgb = sns.color_palette(None, len(set(communities.values())))
    palette = [matplotlib.colors.to_hex(col) for col in rgb]
    for node in communities.keys():
        graph.nodes[node]['color'] = palette[communities[node]]
 """

def find_communities(graph, attrib_cat, partition=None, resolution=1.0, randomize=None, random_state=None):
    #assert isinstance(attrib_cat, Attribute_categorical)
    communities = community_louvain.best_partition(graph, partition=partition, resolution=resolution, randomize=randomize, random_state=random_state)
    assert isinstance(communities, dict)

    n_commu = len(set(communities.values()))

    attrib_cat.categories = [[] for i in range(n_commu)]
    for node, commu in communities.items():
        attrib_cat.categories[commu].append(node)
    attrib_cat.categories.sort(reverse=True, key=len)

    attrib_cat.categories_name = ["Community {} (size: {})".format(i+1, len(attrib_cat.categories[i])) for i in range(n_commu)]
    rgb = sns.color_palette(None, len(set(communities.values())))
    attrib_cat.categories_color = [matplotlib.colors.to_hex(col) for col in rgb]
    attrib_cat.categories_to_keep = [True for i in range(n_commu)]


def betweenness_centrality(graph, k=None, normalized=True, endpoints=False, seed=None):
    btw_central = nx.betweenness_centrality(graph, k=k, normalized=normalized, endpoints=endpoints, seed=seed)
    assert isinstance(btw_central, dict)
    rgb = sns.color_palette(None, len(set(btw_central.values())))
    val = list(set(btw_central.values()))
    palette = [matplotlib.colors.to_hex(col) for col in rgb]
    for node in btw_central.keys():
        graph.nodes[node]['color'] = palette[val.index(btw_central[node])]


def display_data(df):
    res = ""
    for col in df.columns:
        if str(df.iloc[0][col]) != '-':
            res += str(col) + ": " + str(df.iloc[0][col])+"\n"
    return res


if __name__ == "__main__":
    graph, df_node, df_edge = load_graph_from_csv('Data\BIOGRID-PROJECT-glioblastoma_project-GENES.projectindex.txt',
                                                  'Data\BIOGRID-PROJECT-glioblastoma_project-INTERACTIONS.tab3.txt')

    nx = nx.Graph()#Network("500px", "500px")
    nx.add_node(0, label="Node 0")
    nx.add_node(1, label="Node 1", color="blue")
    nx.add_node(2, label="Node 1", color="blue")
    nx.add_edge(0, 1)

    nx.remove_edges_from([(0,1)])


    nt = Network('1080px', '1920px')
    nt.from_nx(nx)
    nt.show("dot.html")
    # shortest_path(107140, 108517, graph)
    # mst = minimum_spanning_tree(graph)
    # find_communities(graph)
    #betweenness_centrality(graph)

    # draw_graph(mst)
    draw_graph(graph)
    #data = df_node.loc[df_node['#BIOGRID ID'] == 106524]
    #print(data)
    #print(display_data(data))
