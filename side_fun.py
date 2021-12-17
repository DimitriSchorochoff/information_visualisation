import networkx as nx
from pyvis.network import Network
import pandas as pd
import community as community_louvain
import seaborn as sns
import matplotlib.colors

# Classes
class Attribute:
    def __init__(self, name, type, related_to_node, init_fun):
        self.name = name
        self.type = type  # Numerical = 0, Categorical = 1, Algorithm = 2
        self.related_to_node = related_to_node

        self.is_init = False
        self.init_fun = init_fun # Graph, Attr -> init all argument properly

    def init_attr(self, graph):
        if not self.is_init:
            self.init_fun(graph, self)
            self.is_init = True

    def reset_attr(self):
        self.is_init = False

    def filter_graph(self, graph):
        pass

    def scale_graph(self, graph):
        pass


class Attribute_numerical(Attribute):
    def __init__(self, name, related_to_node, init_fun, n_decimals=0, min_value=0, max_value=1):
        super().__init__(name, 0, related_to_node, init_fun)
        self.absolute_min_value = min_value
        self.absolute_max_value = max_value
        self.current_min_value = min_value
        self.current_max_value = max_value
        self._filtered_max_value = max_value
        self._filtered_min_value = min_value

        self.n_decimals = n_decimals

        self.colors = ["#6E85B2", "#5C527F", "#3E2C41", "#261C2C"]  # from https://colorhunt.co/palettes/blue
        self.values = {} #Node -> value
        self.scale_with_size = False

    def update_min_max(self):
        # Set initial value
        for a, b in self.values.items():
            self.absolute_min_value = b
            self.absolute_max_value = b
            break

        for a, b in self.values.items():
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
            for n, value in self.values.items():
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

    def init_attr(self, graph):
        save_init = self.is_init
        super().init_attr(graph)

        if not save_init:
            self.update_min_max()

    def reset_attr(self):
        super().reset_attr()
        self.values = {}

        self.absolute_min_value = 0
        self.absolute_max_value = 1
        self.current_min_value = 0
        self.current_max_value = 1
        self._filtered_max_value = 0
        self._filtered_min_value = 1

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
                graph.nodes[n]["size"] = max(1., graph.nodes[n]["size"] * node_scaler)

        else:
            for a, b in graph.edges:
                node_scaler = self.normalize_value(self.values[a][b])
                graph.edges[a][b]["size"] = max(1., graph.edges[a][b]["size"] * node_scaler)


class Attribute_categorical(Attribute):
    def __init__(self, name, related_to_node, init_fun):
        super().__init__(name, 1, related_to_node, init_fun)
        self.categories_name = []
        self.categories_color = []
        self.categories_to_keep = []
        self.categories = []  # List of list of node/edge id

    def init_attr(self, graph):
        save_init = self.is_init
        super().init_attr(graph)

        if not save_init:
            for i in range(len(self.categories_name)):
                self.categories_name[i] = self.categories_name[i] + " (size: {})".format(len(self.categories[i]))

    def reset_attr(self):
        super().reset_attr()
        self.categories_name = []
        self.categories_color = []
        self.categories_to_keep = []
        self.categories = []  # List of list of node/edge id

    def filter_graph(self, graph):
        for i in range(len(self.categories_to_keep)):
            if not self.categories_to_keep[i]:
                if self.related_to_node:
                    graph.remove_nodes_from(self.categories[i])
                else:
                    graph.remove_edges_from(self.categories[i])


class Layout:
    def __init__(self, name, parameter_lst):
        self.name = name
        self.parameter_lst = parameter_lst


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
    nt_graph = Network(height='100%', width='100%')
    nt_graph.from_nx(nx_graph)

    if layout is None or layout.name == LAYOUT_DEFAULT.name:
        nt_graph.toggle_physics(False)
    elif layout.name == LAYOUT_REPULSION.name:
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


def change_all_node_color(graph_save, color):
    assert isinstance(graph_save, nx.Graph)

    for node in graph_save.nodes:
        graph_save.nodes[node]['color'] = color


def change_node_size(graph, node, size):
    assert isinstance(graph, nx.Graph)
    graph.nodes[node]['size'] = size


def change_all_node_size(graph_save, size):
    assert isinstance(graph_save, nx.Graph)

    for node in graph_save.nodes:
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


def change_all_edge_color(graph_save, color):
    assert isinstance(graph_save, nx.Graph)

    for node1, node2 in graph_save.edges:
        graph_save[node1][node2]['color'] = color


def change_edge_width(graph, node1, node2, width):
    assert isinstance(graph, nx.Graph)
    graph[node1][node2]['width'] = width


def change_all_edge_width(graph_save, width):
    assert isinstance(graph_save, nx.Graph)

    for node1, node2 in graph_save.edges:
        graph_save[node1][node2]['width'] = width


def get_edge_color(graph, node1, node2):
    assert isinstance(graph, nx.Graph)
    return graph[node1][node2]['color']


def get_edge_width(graph, node1, node2):
    assert isinstance(graph, nx.Graph)
    return graph[node1][node2]['width']


def attr_degree_init_fun(g, a):
    a.values = dict(g.degree())

def attr_clustering_init_fun(g, a):
    a.values = nx.algorithms.clustering(g)

def attr_find_communities(graph, attrib_cat, partition=None, resolution=2.0, randomize=None, random_state=42):
    # assert isinstance(attrib_cat, Attribute_categorical)
    communities = community_louvain.best_partition(graph, partition=partition, resolution=resolution,
                                                   randomize=randomize, random_state=random_state)
    assert isinstance(communities, dict)

    n_commu = len(set(communities.values()))

    cat = [[] for i in range(n_commu)]
    for node, commu in communities.items():
        cat[commu].append(node)

    # Filter community of size 1
    n_commu = 0
    attrib_cat.categories = []
    for commu in cat:
        if len(commu) > 1:
            n_commu += 1
            attrib_cat.categories.append(commu)

    attrib_cat.categories.sort(reverse=True, key=len)

    attrib_cat.categories_name = ["Community {}".format(i + 1) for i in range(n_commu)]
    rgb = sns.color_palette(None, len(set(communities.values())))
    attrib_cat.categories_color = [matplotlib.colors.to_hex(col) for col in rgb]
    attrib_cat.categories_to_keep = [True for i in range(n_commu)]


def attr_find_min_spanning_tree(graph, attrib_cat):
    st = nx.algorithms.minimum_spanning_tree(graph)

    attrib_cat.categories = [[], []]
    for a, b in graph.edges:
        if st.has_edge(a, b):
            attrib_cat.categories[0].append((a,b))
        else:
            attrib_cat.categories[1].append((a,b))

    attrib_cat.categories_name = ["Edge(s) in", "Edge(s) out"]
    rgb = sns.color_palette(None, 2)
    attrib_cat.categories_color = [matplotlib.colors.to_hex(col) for col in rgb]
    attrib_cat.categories_to_keep = [True for i in range(2)]

def attr_data_node_2_num_factory(df, node_column, val_column):
    def attr_data_node_2_num(graph, attr):
        for n in graph.nodes:
            val = df.loc[(df[node_column] == n)][val_column].values
            if len(val) == 0:
                val = -1
            else:
                val = val[0]
            attr.values[n] = val

    return attr_data_node_2_num

def attr_data_node_2_cat_factory(df, node_column, val_column):
    def attr_data_node_2_cat(graph, attr):
        cat_name = {"None": 0}
        name_counter = 1

        attr.categories = [[]]
        for n in graph.nodes:
            cat = df.loc[(df[node_column] == n)][val_column].values
            if len(cat) == 0:
                cat = "None"
            else:
                cat = str(cat[0])
                if cat == "-": cat = "None"
                if not cat in cat_name:
                    cat_name[cat] = name_counter
                    attr.categories.append([])
                    name_counter += 1

            attr.categories[cat_name[cat]].append(n)

        attr.categories.sort(reverse=True, key=len)

        n_cat = len(cat_name)
        attr.categories_name = [0 for i in range(n_cat)]
        for k, v in cat_name.items():
            attr.categories_name[v] = k

        attr.categories_to_keep = [True for i in range(n_cat)]
        rgb = sns.color_palette(None, n_cat)
        attr.categories_color = [matplotlib.colors.to_hex(col) for col in rgb]

    return attr_data_node_2_cat

def attr_data_edge_2_cat_factory(df, node1_column, node2_column, val_column):
    def attr_data_edge_2_cat(graph, attr):
        cat_name = {"None": 0}
        name_counter = 1

        attr.categories = [[]]
        for a, b in graph.edges:
            cat = df.loc[(df[node1_column] == a)].loc[(df[node2_column] == b)][val_column].values
            if len(cat) == 0:
                cat = "None"
            else:
                cat = str(cat[0])
                if cat == "-": cat = "None"
                if not cat in cat_name:
                    cat_name[cat] = name_counter
                    attr.categories.append([])
                    name_counter += 1

            attr.categories[cat_name[cat]].append((a, b))

        attr.categories.sort(reverse=True, key=len)

        n_cat = len(cat_name)
        attr.categories_name = [0 for i in range(n_cat)]
        for k, v in cat_name.items():
            attr.categories_name[v] = k

        attr.categories_to_keep = [True for i in range(n_cat)]
        rgb = sns.color_palette(None, n_cat)
        attr.categories_color = [matplotlib.colors.to_hex(col) for col in rgb]

    return attr_data_edge_2_cat

def shortest_path(source, target, graph, method='dijkstra'):
    color = get_node_color(graph, source)

    path = nx.algorithms.shortest_path(graph, source=source, target=target, method=method)
    idx = 0
    for i in range(len(path) - 1):
        change_node_color(graph, path[idx], color)
        idx += 1
        change_edge_color(graph, path[i], path[i + 1], color)
    change_node_color(graph, path[idx], color)


def data_node_2_attr_cat(graph, df, attr, node_column, val_column):
    cat_name = {"None": 0}
    name_counter = 1

    attr.categories = [[]]
    for n in graph.nodes:
        cat = df.loc[(df[node_column] == n)][val_column].values
        if len(cat) == 0:
            cat = "None"
        else:
            cat = cat[0]
            if not cat in cat_name:
                cat_name[cat] = name_counter
                attr.categories.append([])
                name_counter += 1

        attr.categories[cat_name[cat]].append(n)

    n_cat = len(cat_name)
    attr.categories_name = [0 for i in range(n_cat)]
    for k, v in cat_name.items():
        attr.categories_name[v] = k

    attr.categories_to_keep = [True for i in range(n_cat)]
    rgb = sns.color_palette(None, n_cat)
    attr.categories_color = [matplotlib.colors.to_hex(col) for col in rgb]
    return


def display_data(df):
    res = ""
    for col in df.columns:
        if str(df.iloc[0][col]) != '-' and str(df.iloc[0][col]) != 'unknown':
            res += f"<strong>{str(col)}</strong>: {str(df.iloc[0][col])}<br>"
    return res
