import networkx

#TODO
def load_graph_from_csv(csv_path):
    #TODO build a networkx graph from csv file
    pass

class Node:
    def __init__(self, graph):
        self.default_color = None
        self.default_show_label = False
        self.default_label_size = 1.
        self.default_label_font = "Arial"
        self.default_scale = 1.

        # TODO initialize with graph
        self.number_nodes = 0

        # TODO initialize with graph
        self.colors = []
        self.show_labels = []
        self.label_sizes = []
        self.label_fonts = []
        self.default_scales = []
        self.names = []

        self.X = []
        self.Y = []


class Edge:
    def __init__(self, graph):
        self.default_color = None
        self.default_show_label = False
        self.default_label_size = 1.
        self.default_label_font = "Arial"
        self.default_scale = 1.

        # TODO initialize with graph
        self.number_nodes = 0

        # TODO initialize with graph
        self.colors = []
        self.show_labels = []
        self.label_sizes = []
        self.label_fonts = []
        self.default_scales = []
        self.names = []

        # TODO initialize with graph
        self.nodes1 = []
        self.nodes2 = []


class Attribute:
    def __init__(self, name, filter_min, filter_max):
        self.name = name
        self.filter_min = filter_min
        self.filter_max = filter_max
        self.color_list = []
        self.is_scaling = False

class Layout:
    pass