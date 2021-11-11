import networkx as nx
from pyvis.network import Network
import pandas as pd
from classes import  *
import matplotlib.pyplot as plt


def load_graph_from_csv(filename_nodes, filename_edges):
    df_node = pd.read_csv(filename_nodes, sep='\t')
    df_edge = pd.read_csv(filename_edges, sep='\t', low_memory=False)
    nodes_attr = df_node.columns.values.tolist()
    edges_attr = df_edge.columns.values.tolist()
    lst_nodes, lst_edges = [], []
    mem = []

    for i in range(len(df_node.index)):
        lst_nodes.append((int(df_node[nodes_attr[0]][i]), {nodes_attr[j]: df_node[nodes_attr[j]][i] for j in range(1,len(nodes_attr))}))

    special_index = [i for i in range(len(edges_attr))]
    special_index.remove(3), special_index.remove(4)

    for i in range(len(df_edge.index)):
        if (df_edge[edges_attr[3]][i], df_edge[edges_attr[4]][i]) not in mem: #Check if the edge is already in the list
            lst_edges.append((int(df_edge[edges_attr[3]][i]), int(df_edge[edges_attr[4]][i]),{edges_attr[j]: df_edge[edges_attr[j]][i] for j in special_index}))
            mem.append((df_edge[edges_attr[3]][i], df_edge[edges_attr[4]][i]))
            mem.append((df_edge[edges_attr[4]][i], df_edge[edges_attr[3]][i]))

        if df_edge[edges_attr[3]][i] not in lst_nodes[:][0]:
            lst_nodes.append((int(df_edge[edges_attr[3]][i]), {}))
        if df_edge[edges_attr[4]][i] not in lst_nodes[:][0]:
            lst_nodes.append((int(df_edge[edges_attr[4]][i]), {}))


    G = nx.Graph()
    G.add_nodes_from([i[0] for i in lst_nodes])
    G.add_edges_from([i[:2] for i in lst_edges])

    return G


def draw_graph(nx_graph):
    nt_graph = Network('1080px', '1920px')
    nt_graph.from_nx(nx_graph)
    #nt_graph.show('nx.html')
    nt_graph.save_graph('nx.html')



def shortest_path(source, dest, graph):
    #use a etworkx function
    pass

def draw_graph_layout(layout, graph):
    #use networkx layouts
    #one function by layout
    pass

def add_node(graph, name, color, size, neighbourds):
    #add a node to networkx graph
    pass

def add_edge(graph, name, color, size, node1, node2):
    #add edge to networkx
    pass

def change_node_color(node, color):
    pass

def change_node_size(node, size):
    pass

def change_edge_color(edge, color):
    pass

def change_edge_size(edge, size):
    pass

def clustering_coefficient(graph):
    pass

def betweenness_centrality(graph):
    pass

def minimum_spanning_tree(graph):
    pass

def find_communities(graph):
    pass

def filter(graph):
    pass


graph = load_graph_from_csv('Data/BIOGRID-PROJECT-glioblastoma_project-GENES.projectindex.csv', 'Data/BIOGRID-PROJECT-glioblastoma_project-INTERACTIONS.tab3.csv')
draw_graph(graph)
