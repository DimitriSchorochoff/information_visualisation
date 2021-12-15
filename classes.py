import networkx


# TODO
def load_graph_from_csv(csv_path):
    # TODO build a networkx graph from csv file
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
    def __init__(self, name, type, related_to_node):
        self.name = name
        self.type = type  # Numerical = 0, Categorical = 1, Algorithm = 2
        self.related_to_node = related_to_node

        self.is_init = False

    def filter_graph(self, graph):
        pass

    def scale_graph(self, graph):
        pass


class Attribute_numerical(Attribute):
    def __init__(self, name, min_value, max_value, related_to_node):
        super().__init__(name, 0, related_to_node)
        self.absolute_min_value = min_value
        self.absolute_max_value = max_value
        self.current_min_value = min_value
        self.current_max_value = max_value
        self._filtered_max_value = max_value
        self._filtered_min_value = min_value

        self.colors = ["#6E85B2", "#5C527F", "#3E2C41", "#261C2C"]  # from https://colorhunt.co/palettes/blue
        self.values = {}
        self.scale_with_size = False

    def update_min_max(self):
        # Set initial value
        for a, b in self.values:
            self.absolute_min_value = b
            self.absolute_max_value = b
            break

        for a, b in self.values:
            if b < self.absolute_min_value:
                self.absolute_min_value = b
            elif b > self.absolute_max_value:
                self.absolute_max_value = b

        self.current_min_value = self.absolute_min_value
        self.current_max_value = self.absolute_max_value

    def normalize_value(self, value):
        return (value - self._filtered_min_value) / self._filtered_max_value

    def get_color_index(self, value):
        n_color = len(self.colors)
        portion = (self._filtered_max_value - self._filtered_min_value) / n_color
        for i in range(n_color - 1):
            if self._filtered_min_value + i * portion <= value <= self._filtered_min_value + (i + 1) * portion:
                return i
        return n_color - 1

    def set_filtered_min_max(self):
        # Compute new min and max value after the filter to have proper normalization
        self._filtered_min_value = self.absolute_max_value
        self._filtered_max_value = self.absolute_min_value

        if self.related_to_node:
            for n, value in self.values:
                if self.current_min_value < value < self.current_max_value:
                    if value > self._filtered_max_value:
                        self._filtered_max_value = value
                    if value < self._filtered_min_value:
                        self._filtered_min_value = value

        else:
            for t, v in self.values.keys():
                if self.current_min_value < self.values[t[0]][t[1]] < self.current_max_value:
                    if self.values[t[0]][t[1]] > self._filtered_max_value:
                        self._filtered_max_value = self.values[t[0]][t[1]]
                    if self.values[t[0]][t[1]] < self._filtered_min_value:
                        self._filtered_min_value = self.values[v][t[1]]

    def filter_graph(self, graph):
        if self.absolute_min_value == self.current_min_value and self.absolute_max_value == self.current_max_value:
            return

        # Compute new min and max value after the filter to have proper normalization
        self._filtered_min_value = self.absolute_max_value
        self._filtered_max_value = self.absolute_min_value

        if self.related_to_node:
            nodes_to_remove = []
            for n in graph.nodes:
                if (self.values[n] < self.current_min_value) or (self.current_max_value < self.values[n]):
                    nodes_to_remove.append(n)
                else:
                    if self.values[n] > self._filtered_max_value:
                        self._filtered_max_value = self.values[n]
                    if self.values[n] < self._filtered_min_value:
                        self._filtered_min_value = self.values[n]

            graph.remove_nodes_from(nodes_to_remove)

        else:
            edges_to_remove = []
            for a, b in graph.edges:
                if (self.values[a][b] < self.current_min_value) or (self.current_max_value < self.values[a][b]):
                    edges_to_remove.append((a, b))
                else:
                    if self.values[a][b] > self._filtered_max_value:
                        self._filtered_max_value = self.values[a][b]
                    elif self.values[a][b] < self._filtered_min_value:
                        self._filtered_min_value = self.values[a][b]

            graph.remove_edges_from(edges_to_remove)

    def scale_graph(self, graph):
        if not self.scale_with_size: return

        if self.related_to_node:
            for n in graph.nodes:
                node_scaler = self.normalize_value(self.values[n])
                graph.nodes[n]["size"] = max(1., graph.nodes[n]["size"] * node_scaler * 10)

        else:
            for a, b in graph.edges:
                node_scaler = self.normalize_value(self.values[a][b])
                graph.edges[a][b]["size"] = max(1., graph.edges[a][b]["size"] * node_scaler * 10)


class Attribute_categorical(Attribute):
    def __init__(self, name, related_to_node):
        super().__init__(name, 1, related_to_node)
        self.categories_name = []
        self.categories_color = []
        self.categories_to_keep = []
        self.categories = []  # List of list of node/edge id

    """
        def smooth_name_len(self):
        len_max = 0
        for s in self.categories_name:
            current_len = len(s)
            if current_len > len_max:
                len_max = current_len

        print(len_max)
        for i in range(len(self.categories_name)):
            len_diff = len_max - len(self.categories_name[i])
            print(len_diff)
            self.categories_name[i] = self.categories_name[i] + (" " * (len_diff+1)) + ":"
            print(len(self.categories_name[i] ))
    """

    def filter_graph(self, graph):
        for i in range(len(self.categories_to_keep)):
            if not self.categories_to_keep[i]:
                if self.related_to_node:
                    graph.remove_nodes_from(self.categories[i])
                else:
                    graph.remove_edges_from(self.categories[i])


class Attribute_algorithm(Attribute):
    def __init__(self, name, default_color):
        super().__init__(name, 2)
        self.color = default_color


class Layout:
    def __init__(self, name, parameter_lst):
        self.name = name
        self.parameter_lst = parameter_lst

    def return_coordinate(self, graph):
        # Renvoi un tuple ([coord X], [coord Y])
        pass


class Layout_parameter:
    def __init__(self, name, data_type):
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
