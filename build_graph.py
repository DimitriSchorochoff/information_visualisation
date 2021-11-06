import networkx as nx
from pyvis.network import Network
from classes import  *

#TODO
def load_graph_from_csv(filename_nodes, filename_edges):
    #add nodes
    #add edges
    pass

def draw_graph(graph):
    #transform a networkx into pyvis
    pass

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







nx_graph = nx.complete_graph(200)

nt = Network("1080x", "1820px")
# populates the nodes and edges data structures
nt.from_nx(nx_graph)
nt.show("nx.html")
