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
    def __init__(self, name, filter_min, filter_max, isCategorical):
        self.name = name
        self.filter_min = filter_min
        self.filter_max = filter_max
        self.color_list = []
        self.is_categorical = isCategorical
        self.is_scaling = False

class Layout:
    def __init__(self, name, parameter_lst):
        self.name = name
        self.parameter_lst = parameter_lst

    def return_coordinate(self, graph):
        #Renvoi un tuple ([coord X], [coord Y])
        pass

class Layout_parameter:
    def __init__(self, name,  data_type):
        self.name = name
        self.data_type = data_type
        # 0 Layout_parameter_value, 1 Layout_parameter_boolean, 2 Layout_parameter_categorical


class Layout_parameter_value(Layout_parameter):
    def __init__(self, name, minimum, maximum, start, step):
        super().__init__(name, 0)
        self.minimum = minimum
        self.maximum = maximum
        self.start = start
        self.step = step

class Layout_parameter_boolean(Layout_parameter):
    def __init__(self, name):
        super().__init__(name, 1)
        self.coched = False

class Layout_parameter_categorical(Layout_parameter):
    def __init__(self, name, list_choice, start_choice_pos):
        super().__init__(name, 2)
        self.list_choice = list_choice
        self.start_choice_pos = start_choice_pos
