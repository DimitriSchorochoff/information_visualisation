import networkx as nx
import pandas as pd
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal, Qt, pyqtSlot, QSortFilterProxyModel
from PyQt5.QtWidgets import QCompleter, QComboBox
import pathlib
from PyQt5.QtWidgets import QMessageBox, QColorDialog
import sys

import side_fun
import copy
from qtrangeslider._labeled import EdgeLabelMode, QLabeledDoubleRangeSlider

STR_ALL_NODES = "### All nodes ###"
STR_ALL_EDGES = "### All edges ###"

FILE_NODES_PATH = None
FILE_EDGES_PATH = None
FILE_CHEMICALS_PATH = None
FILE_PTM_PATH = None
DEBUG = True

if DEBUG:
    #FILE_NODES_PATH = r"d:\Users\Home\Documents\Unif\M1 Q1\information_visualisation\Data\BIOGRID-PROJECT-glioblastoma_project-GENES.projectindex.txt"
    #FILE_EDGES_PATH = r"d:\Users\Home\Documents\Unif\M1 Q1\information_visualisation\Data\BIOGRID-PROJECT-glioblastoma_project-INTERACTIONS.tab3.txt"
    #FILE_CHEMICALS_PATH = r"d:\Users\Home\Documents\Unif\M1 Q1\information_visualisation\Data\BIOGRID-PROJECT-glioblastoma_project-CHEMICALS.chemtab.txt"
    #FILE_PTM_PATH = r"d:\Users\Home\Documents\Unif\M1 Q1\information_visualisation\Data\BIOGRID-PROJECT-glioblastoma_project-PTM.ptmtab.txt"
    FILE_NODES_PATH = r"C:\Users\dimis\OneDrive\Documents\GitHub\information_visualisation\Data\BIOGRID-PROJECT-glioblastoma_project-GENES.projectindex.txt"
    FILE_EDGES_PATH = r"C:\Users\dimis\OneDrive\Documents\GitHub\information_visualisation\Data\BIOGRID-PROJECT-glioblastoma_project-INTERACTIONS.tab3.txt"
    FILE_CHEMICALS_PATH = r"C:\Users\dimis\OneDrive\Documents\GitHub\information_visualisation\Data\BIOGRID-PROJECT-glioblastoma_project-CHEMICALS.chemtab.txt"
    FILE_PTM_PATH = r"C:\Users\dimis\OneDrive\Documents\GitHub\information_visualisation\Data\BIOGRID-PROJECT-glioblastoma_project-PTM.ptmtab.txt"


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        # Init graph + df
        self.graph_current, self.df_node, self.df_edge = side_fun.load_graph_from_csv(FILE_NODES_PATH,
                                                                                         FILE_EDGES_PATH)
        self.graph_original = copy.deepcopy(self.graph_current)
        self.df_chemicals = pd.read_csv(FILE_CHEMICALS_PATH, sep='\t')
        self.df_ptm = pd.read_csv(FILE_PTM_PATH, sep='\t')

        self.list_layout = [side_fun.LAYOUT_DEFAULT, side_fun.LAYOUT_BARNES, side_fun.LAYOUT_FORCEATLAS,
                            side_fun.LAYOUT_REPULSION]

        self.list_attribute = self.init_list_attr()

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.splitter = QtWidgets.QSplitter(MainWindow)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setStretchFactor(1, 1)
        self.verticalLayout.addWidget(self.splitter)

        self.webEngineView = QtWebEngineWidgets.QWebEngineView(self.centralwidget)

        self.splitter.addWidget(self.webEngineView)

        self.main_tab_widget = QtWidgets.QTabWidget(self.centralwidget)
        self.main_tab_widget.setObjectName("main_tab_widget")
        self.main_tab_widget.tabBarClicked.connect(self.on_tab_clicked)

        self.tab_layout = QtWidgets.QWidget()
        self.tab_layout.setObjectName("tab_layout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab_layout)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.layout_layout_left = QtWidgets.QVBoxLayout()
        self.layout_layout_left.setObjectName("layout_layout_left")
        self.layout_filter_layout = QtWidgets.QHBoxLayout()
        self.layout_filter_layout.setObjectName("layout_filter_layout")
        self.layout_filter_line_edit = QtWidgets.QLineEdit(self.tab_layout)
        self.layout_filter_line_edit.setObjectName("layout_filter_line_edit")
        self.layout_filter_layout.addWidget(self.layout_filter_line_edit)

        self.layout_filter_button = QtWidgets.QPushButton(self.tab_layout)
        self.layout_filter_button.setObjectName("layout_filter_button")
        self.layout_filter_button.clicked.connect(
            lambda: self.selection_list_filter(self.layout_selection_list, self.layout_filter_line_edit.text()))
        self.layout_filter_layout.addWidget(self.layout_filter_button)

        self.layout_layout_left.addLayout(self.layout_filter_layout)
        self.layout_selection_list = QtWidgets.QListWidget(self.tab_layout)
        self.layout_selection_list.itemClicked.connect(
            lambda item: self.layout_selection_list_on_item_click(self.layout_selection_list.currentRow()))
        self.layout_selection_list.setObjectName("layout_selection_list")
        self.layout_layout_left.addWidget(self.layout_selection_list)
        self.horizontalLayout_2.addLayout(self.layout_layout_left, 4)

        self.layout_layout_right = QtWidgets.QVBoxLayout()
        self.layout_layout_right.setObjectName("layout_layout_right")
        self.layout_layout_right_widget_lst = []

        self.layout_widget_right = QtWidgets.QWidget()
        self.layout_widget_right.setLayout(self.layout_layout_right)

        self.layout_scroll_area = QtWidgets.QScrollArea()
        self.layout_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.layout_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.layout_scroll_area.setWidgetResizable(True)
        self.layout_scroll_area.setWidget(self.layout_widget_right)

        self.horizontalLayout_2.addWidget(self.layout_scroll_area, 6)

        self.layout_build_button = QtWidgets.QPushButton(self.tab_layout)
        self.layout_build_button.setObjectName("layout_build_button")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.layout_build_button.sizePolicy().hasHeightForWidth())
        self.layout_build_button.setSizePolicy(sizePolicy)
        self.layout_build_button.clicked.connect(self.runComputeAndDisplayGraph)
        self.horizontalLayout_2.addWidget(self.layout_build_button, 1)
        self.main_tab_widget.addTab(self.tab_layout, "")

        self.tab_attr = QtWidgets.QWidget()
        self.tab_attr.setObjectName("tab_attrib")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab_attr)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tab_attr_vertical_left = QtWidgets.QVBoxLayout()
        self.tab_attr_vertical_left.setObjectName("tab_attr_vertical_left")
        self.attr_filter_attr_layout = QtWidgets.QHBoxLayout()
        self.attr_filter_attr_layout.setObjectName("attr_filter_attr_layout")
        self.atttr_filter_attr_line_edit = QtWidgets.QLineEdit(self.tab_attr)
        self.atttr_filter_attr_line_edit.setObjectName("atttr_filter_attr_line_edit")
        self.attr_filter_attr_layout.addWidget(self.atttr_filter_attr_line_edit)
        self.attr_filter_attr_button = QtWidgets.QPushButton(self.tab_attr)
        self.attr_filter_attr_button.setObjectName("attr_filter_attr_button")
        self.attr_filter_attr_button.clicked.connect(
            lambda: self.selection_list_filter(self.attr_selection_list, self.atttr_filter_attr_line_edit.text()))
        self.attr_filter_attr_layout.addWidget(self.attr_filter_attr_button)
        self.tab_attr_vertical_left.addLayout(self.attr_filter_attr_layout, 4)

        self.attr_selection_list = QtWidgets.QListWidget(self.tab_attr)
        self.attr_selection_list.setObjectName("attr_selection_list")
        self.attr_selection_list.itemClicked.connect(self.attr_selection_list_on_item_click)
        self.tab_attr_vertical_left.addWidget(self.attr_selection_list)
        self.horizontalLayout.addLayout(self.tab_attr_vertical_left)
        self.tab_attr_vertical_right = QtWidgets.QVBoxLayout()
        self.tab_attr_vertical_right.setObjectName("tab_attr_vertical_right")

        # Numerical widget
        self.attr_scale_with_size_hlayout = QtWidgets.QHBoxLayout()
        self.attr_scale_with_size_hlayout.setObjectName("attr_scale_with_size_hlayout")

        self.attr_scale_with_size_checkbox = QtWidgets.QCheckBox(self.tab_attr)
        self.attr_scale_with_size_checkbox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.attr_scale_with_size_checkbox.setObjectName("attr_scale_with_size_checkbox")
        self.attr_scale_with_size_hlayout.addWidget(self.attr_scale_with_size_checkbox)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.attr_scale_with_size_hlayout.addItem(spacerItem)
        self.tab_attr_vertical_right.addLayout(self.attr_scale_with_size_hlayout)
        self.attr_slider_hlayout = QtWidgets.QHBoxLayout()
        self.attr_slider_hlayout.setObjectName("attr_slider_hlayout")
        self.attr_filter_label = QtWidgets.QLabel(self.tab_attr)
        self.attr_filter_label.setObjectName("attr_filter_label")
        self.attr_slider_hlayout.addWidget(self.attr_filter_label)
        self.attr_filter_range_slider = QLabeledDoubleRangeSlider(self.tab_attr)
        self.attr_filter_range_slider.setOrientation(QtCore.Qt.Horizontal)
        self.attr_filter_range_slider.setEdgeLabelMode(EdgeLabelMode.NoLabel)
        self.attr_filter_range_slider.setObjectName("attr_filter_range_slider")
        self.attr_slider_hlayout.addWidget(self.attr_filter_range_slider)
        self.tab_attr_vertical_right.addLayout(self.attr_slider_hlayout)

        self.attr_num_layout_widget_lst = []
        self.attr_num_color_hlayout = QtWidgets.QHBoxLayout()
        self.attr_num_color_hlayout.setObjectName("attr_num_color_hlayout")
        self.tab_attr_vertical_right.addLayout(self.attr_num_color_hlayout)

        # Categorical widget
        self.attr_cat_layout = QtWidgets.QVBoxLayout()
        self.attr_cat_layout.setObjectName("attrib_cat_layout")
        self.attr_cat_layout_widget_lst = []

        self.attr_cat_widgets = QtWidgets.QWidget()
        self.attr_cat_widgets.setLayout(self.attr_cat_layout)

        self.attr_scroll_area = QtWidgets.QScrollArea()
        self.attr_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.attr_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.attr_scroll_area.setWidgetResizable(True)
        self.attr_scroll_area.setWidget(self.attr_cat_widgets)
        self.attr_scroll_area.setVisible(False)
        self.tab_attr_vertical_right.addWidget(self.attr_scroll_area, 6)

        self.attr_lower_hlayout = QtWidgets.QHBoxLayout(self.tab_attr)

        self.attr_apply_color_button = QtWidgets.QPushButton()
        self.attr_apply_color_button.setObjectName("attr_apply_color_button")
        self.attr_lower_hlayout.addWidget(self.attr_apply_color_button, 3)

        self.attr_delete_nodes_button = QtWidgets.QPushButton()
        self.attr_delete_nodes_button.setObjectName("attr_delete_nodes")
        self.attr_lower_hlayout.addWidget(self.attr_delete_nodes_button, 3)
        self.attr_delete_nodes_button.clicked.connect(self.delete_unfiltered)

        self.attr_reset_graph_button = QtWidgets.QPushButton()
        self.attr_reset_graph_button.setObjectName("attr_reset_graph")
        self.attr_lower_hlayout.addWidget(self.attr_reset_graph_button, 3)
        self.tab_attr_vertical_right.addLayout(self.attr_lower_hlayout, 1)
        self.attr_reset_graph_button.clicked.connect(self.reset_graph)

        self.horizontalLayout.addLayout(self.tab_attr_vertical_right, 6)

        self.attr_build_button = QtWidgets.QPushButton(self.tab_layout)
        self.attr_build_button.setObjectName("attrib_build_button")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.attr_build_button.sizePolicy().hasHeightForWidth())
        self.attr_build_button.setSizePolicy(sizePolicy)
        self.attr_build_button.clicked.connect(self.runComputeAndDisplayGraph)
        self.horizontalLayout.addWidget(self.attr_build_button, 1)

        self.main_tab_widget.addTab(self.tab_attr, "")

        self.tab_node = QtWidgets.QWidget()
        self.tab_node.setObjectName("tab_node_edge")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab_node)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.node_vlayout_left = QtWidgets.QVBoxLayout()
        self.node_vlayout_left.setObjectName("node_vlayout_left")
        self.node_filter_hlayout = QtWidgets.QHBoxLayout()
        self.node_filter_hlayout.setObjectName("node_filter_hlayout")
        self.node_filter_edit = QtWidgets.QLineEdit(self.tab_node)
        self.node_filter_edit.setObjectName("node_filter_edit")
        self.node_filter_hlayout.addWidget(self.node_filter_edit)

        self.node_filter_button = QtWidgets.QPushButton(self.tab_node)
        self.node_filter_button.setObjectName("node_filter_button")
        self.node_filter_button.clicked.connect(
            lambda: self.selection_list_filter(self.node_selection_list, self.node_filter_edit.text()))

        self.node_filter_hlayout.addWidget(self.node_filter_button)
        self.node_vlayout_left.addLayout(self.node_filter_hlayout)
        self.node_selection_list = QtWidgets.QListWidget(self.tab_node)
        self.node_selection_list.setObjectName("node_selection_list")
        self.node_vlayout_left.addWidget(self.node_selection_list)
        self.horizontalLayout_3.addLayout(self.node_vlayout_left, 4)
        self.node_selection_list.itemClicked.connect(self.node_selection_list_on_item_click)
        self.node_selection_list.itemDoubleClicked.connect(
            lambda item: self.node_selection_list_on_item_double_click(self.node_selection_list.currentItem()))

        self.node_vlayout_right = QtWidgets.QVBoxLayout()
        self.node_vlayout_right.setObjectName("node_vlayout_right")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)

        self.tab_node_color_hlayout = QtWidgets.QHBoxLayout(self.tab_node)
        self.tab_node_color_hlayout.setObjectName("tab_node_color_hlayout")

        self.tab_node_color_label = QtWidgets.QLabel()
        self.tab_node_color_label.setObjectName("tab_node_color_label")
        self.tab_node_color_hlayout.addWidget(self.tab_node_color_label)

        self.tab_node_color_button = QtWidgets.QPushButton()
        self.tab_node_color_button.setObjectName("tab_node_color_button")
        self.tab_node_color_button.setFlat(True)
        self.tab_node_color_hlayout.addWidget(self.tab_node_color_button)
        self.verticalLayout_3.addLayout(self.tab_node_color_hlayout)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.tab_node)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.node_size_spinbox = QtWidgets.QDoubleSpinBox(self.tab_node)
        self.node_size_spinbox.setObjectName("node_size_spinbox")
        self.horizontalLayout_4.addWidget(self.node_size_spinbox)

        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)

        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.node_vlayout_right.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")

        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem7)
        self.node_vlayout_right.addLayout(self.verticalLayout_2)

        self.node_shortest_path_hlayout = QtWidgets.QHBoxLayout(self.tab_node)
        self.node_shortest_path_hlayout.setObjectName("node_shortest_path_label")

        self.node_shortest_path_label = QtWidgets.QLabel(self.tab_node)
        self.node_shortest_path_label.setObjectName("node_shortest_path_label")
        self.node_shortest_path_hlayout.addWidget(self.node_shortest_path_label)

        self.node_shortest_path_to_combo = ExtendedComboBox(self.tab_node)
        self.node_shortest_path_hlayout.addWidget(self.node_shortest_path_to_combo)

        self.node_shortest_path_button = QtWidgets.QPushButton(self.tab_node)
        self.node_shortest_path_button.setObjectName("node_shortest_path_button")
        self.node_shortest_path_hlayout.addWidget(self.node_shortest_path_button)

        self.node_vlayout_right.addLayout(self.node_shortest_path_hlayout)


        self.horizontalLayout_3.addLayout(self.node_vlayout_right, 6)

        self.node_build_button = QtWidgets.QPushButton(self.tab_layout)
        self.node_build_button.setObjectName("node_build_button")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.node_build_button.sizePolicy().hasHeightForWidth())
        self.node_build_button.setSizePolicy(sizePolicy)
        self.node_build_button.clicked.connect(self.runComputeAndDisplayGraph)
        self.horizontalLayout_3.addWidget(self.node_build_button, 1)

        self.main_tab_widget.addTab(self.tab_node, "")

        self.tab_edge = QtWidgets.QWidget()
        self.tab_edge.setObjectName("tab_edge")
        self.edge_hlayout = QtWidgets.QHBoxLayout(self.tab_edge)
        self.edge_hlayout.setObjectName("edge_hlayout")
        self.edge_vlayout_left = QtWidgets.QVBoxLayout()
        self.edge_vlayout_left.setObjectName("edge_vlayout_left")
        self.edge_filter_hlayout = QtWidgets.QHBoxLayout()
        self.edge_filter_hlayout.setObjectName("edge_filter_hlayout")
        self.edge_filter_edit = QtWidgets.QLineEdit(self.tab_edge)
        self.edge_filter_edit.setObjectName("edge_filter_edit")
        self.edge_filter_hlayout.addWidget(self.edge_filter_edit)

        self.edge_filter_button = QtWidgets.QPushButton(self.tab_edge)
        self.edge_filter_button.setObjectName("edge_filter_button")
        self.edge_filter_button.clicked.connect(
            lambda: self.selection_list_filter(self.edge_selection_list, self.edge_filter_edit.text()))

        self.edge_filter_hlayout.addWidget(self.edge_filter_button)
        self.edge_vlayout_left.addLayout(self.edge_filter_hlayout)
        self.edge_selection_list = QtWidgets.QListWidget(self.tab_edge)
        self.edge_selection_list.setObjectName("edge_selection_list")
        self.edge_vlayout_left.addWidget(self.edge_selection_list)
        self.edge_hlayout.addLayout(self.edge_vlayout_left, 4)
        self.edge_selection_list.itemClicked.connect(self.edge_selection_list_on_item_click)
        self.edge_selection_list.itemDoubleClicked.connect(
            lambda item: self.edge_selection_list_on_item_double_click(self.edge_selection_list.currentItem()))

        self.edge_vlayout_right = QtWidgets.QVBoxLayout()
        self.edge_vlayout_right.setObjectName("edge_vlayout_right")
        self.edge_verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.edge_verticalLayout_3.setObjectName("edge_verticalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.edge_verticalLayout_3.addItem(spacerItem1)

        self.tab_edge_color_hlayout = QtWidgets.QHBoxLayout(self.tab_edge)
        self.tab_edge_color_hlayout.setObjectName("tab_edge_color_hlayout")

        self.tab_edge_color_label = QtWidgets.QLabel()
        self.tab_edge_color_label.setObjectName("tab_edge_color_label")
        self.tab_edge_color_hlayout.addWidget(self.tab_edge_color_label)

        self.tab_edge_color_button = QtWidgets.QPushButton()
        self.tab_edge_color_button.setObjectName("tab_edge_color_button")
        self.tab_edge_color_button.setFlat(True)
        self.tab_edge_color_hlayout.addWidget(self.tab_edge_color_button)
        self.edge_verticalLayout_3.addLayout(self.tab_edge_color_hlayout)

        self.edge_horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.edge_horizontalLayout_4.setObjectName("edge_horizontalLayout_4")
        self.edge_label_4 = QtWidgets.QLabel(self.tab_edge)
        self.edge_label_4.setObjectName("edge_label_4")
        self.edge_horizontalLayout_4.addWidget(self.edge_label_4)
        self.edge_size_spinbox = QtWidgets.QDoubleSpinBox(self.tab_edge)
        self.edge_size_spinbox.setObjectName("edge_size_spinbox")
        self.edge_horizontalLayout_4.addWidget(self.edge_size_spinbox)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.edge_horizontalLayout_4.addItem(spacerItem2)
        self.edge_verticalLayout_3.addLayout(self.edge_horizontalLayout_4)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.edge_verticalLayout_3.addItem(spacerItem3)
        self.edge_vlayout_right.addLayout(self.edge_verticalLayout_3)
        self.edge_verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.edge_verticalLayout_2.setObjectName("edge_verticalLayout_2")
        edge_spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.edge_verticalLayout_2.addItem(edge_spacerItem7)
        self.edge_vlayout_right.addLayout(self.edge_verticalLayout_2)
        self.edge_hlayout.addLayout(self.edge_vlayout_right, 6)

        self.edge_build_button = QtWidgets.QPushButton(self.tab_layout)
        self.edge_build_button.setObjectName("edge_build_button")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edge_build_button.sizePolicy().hasHeightForWidth())
        self.edge_build_button.setSizePolicy(sizePolicy)
        self.edge_build_button.clicked.connect(self.runComputeAndDisplayGraph)
        self.edge_hlayout.addWidget(self.edge_build_button, 1)

        self.main_tab_widget.addTab(self.tab_edge, "")
        self.splitter.addWidget(self.main_tab_widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.main_tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Set default qsplitter size
        self.splitter.setSizes([400, 50])

        self.init_selection_lists()


    def init_list_attr(self):
        attr_lst = []
        attr_lst.append(side_fun.Attribute_numerical("Degree", True, side_fun.attr_degree_init_fun, 0))
        attr_lst.append(
            side_fun.Attribute_numerical("Clustering coefficient", True, side_fun.attr_clustering_init_fun, 0))
        attr_lst.append(side_fun.Attribute_categorical("Communities", True, side_fun.attr_find_communities))
        attr_lst.append(side_fun.Attribute_categorical("Minimum spanning tree", False, side_fun.attr_find_min_spanning_tree))

        # Node db
        column_cat = ["CATEGORY VALUES", "OFFICIAL SYMBOL", "SUBCATEGORY VALUES"]
        for c in column_cat:
            attr_lst.append(side_fun.Attribute_categorical("Node: {}".format(c), True,
                                                              side_fun.attr_data_node_2_cat_factory(self.df_node,
                                                                                                       "#BIOGRID ID", c)))
        column_num = ["INTERACTION COUNT", "PTM COUNT", "CHEMICAL INTERACTION COUNT"]
        for c in column_num:
            attr_lst.append(side_fun.Attribute_numerical("Node: {}".format(c), True,
                                                            side_fun.attr_data_node_2_num_factory(self.df_node,
                                                                                                     "#BIOGRID ID", c), 0))

        """
        #Edge db
        column_cat = ["Experimental System", "Experimental System Type", "Author", "Throughput", "Modification", "Ontology Term Names", "Ontology Term Categories", "Ontology Term Qualifier Names", "Ontology Term Types"]
        for c in column_cat:
            attr_lst.append(side_fun.Attribute_categorical("Edge: {}".format(c), True,
                                                            side_fun.attr_data_node_2_cat_factory(self.df_chemicals,
                                                                                                     "BioGRID Gene ID", c)))
        """

        #Chem db
        column_cat = ["Systematic Name", "Official Symbol", "Action", "Interaction Type", "Author", "Chemical Name", "Chemical Brands", "Chemical Source", "Molecular Formula", "Chemical Type", "ATC Codes", "Curated By", "Method", "Related Systematic Name", "Related Official Symbol"]
        for c in column_cat:
            attr_lst.append(side_fun.Attribute_categorical("Chem: {}".format(c), True,
                                                            side_fun.attr_data_node_2_cat_factory(self.df_chemicals,
                                                                                                     "BioGRID Gene ID", c)))

        #PTM db
        column_cat = ["Systematic Name", "Official Symbol", "Post Translational Modification", "Residue", "Author", "Has Relationships", "Source Database"]
        for c in column_cat:
            attr_lst.append(side_fun.Attribute_categorical("PTM: {}".format(c), True,
                                                            side_fun.attr_data_node_2_cat_factory(self.df_ptm,
                                                                                                     "BioGRID ID", c)))

        return attr_lst

    def init_selection_lists(self):
        self.layout_selection_list_init()
        self.attr_selection_list_init()
        self.node_selection_list_init()
        self.edge_selection_list_init()

    def update_selection_list(self):
        self.main_tab_widget.setCurrentIndex(0)
        self.layout_selection_list_update()
        self.attr_selection_list_update()
        self.node_selection_list_update()
        self.edge_selection_list_update()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GraphX"))
        self.layout_filter_button.setText(_translate("MainWindow", "Filter"))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tab_layout),
                                        _translate("MainWindow", "Layout"))
        self.attr_filter_attr_button.setText(_translate("MainWindow", "Filter"))
        self.attr_scale_with_size_checkbox.setText(_translate("MainWindow", "Scale with size"))
        self.attr_filter_label.setText(_translate("MainWindow", "Filter"))
        self.attr_apply_color_button.setText(_translate("MainWindow", "Apply color"))
        self.attr_delete_nodes_button.setText(_translate("MainWindow", "Delete unfiltered"))
        self.attr_reset_graph_button.setText(_translate("MainWindow", "Reset graph"))

        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tab_attr),
                                        _translate("MainWindow", "Attribute"))
        self.node_filter_button.setText(_translate("MainWindow", "Filter"))
        self.edge_filter_button.setText(_translate("MainWindow", "Filter"))
        self.tab_node_color_button.setText(_translate("MainWindow", " "))
        self.tab_node_color_label.setText(_translate("MainWindow", "Pick a color: "))
        self.tab_edge_color_label.setText(_translate("MainWindow", "Pick a color: "))
        self.tab_edge_color_button.setText(_translate("MainWindow", " "))
        self.label_4.setText(_translate("MainWindow", "Node size"))
        self.edge_label_4.setText(_translate("MainWindow", "Edge size"))

        self.node_shortest_path_label.setText(_translate("MainWindow", "Color shortest path to:"))
        self.node_shortest_path_button.setText(_translate("MainWindow", "Apply"))

        self.layout_build_button.setText(_translate("MainWindow", "Build"))
        self.attr_build_button.setText(_translate("MainWindow", "Build"))
        self.edge_build_button.setText(_translate("MainWindow", "Build"))
        self.node_build_button.setText(_translate("MainWindow", "Build"))

        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tab_node), _translate("MainWindow", "Node"))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tab_edge),
                                        _translate("MainWindow", "Edge"))

    def delete_unfiltered(self):
        for a in self.list_attribute:
            a.filter_graph(self.graph_current)
            a.reset_attr()

        self.update_selection_list()

    def reset_graph(self):
        self.graph_current = copy.deepcopy(self.graph_original)
        self.init_selection_lists()

        for a in self.list_attribute:
            a.reset_attr()

        self.update_selection_list()

    class Graph_computer_worker(QObject):
        finished = pyqtSignal()

        def __init__(self, ui_window):
            super().__init__()
            self.ui_window = ui_window

        def run(self):
            """Long-running task."""
            # Change button display

            current_layout_pos = self.ui_window.layout_selection_list.currentRow()
            if current_layout_pos == -1:
                current_layout = None
            else:
                current_layout = self.ui_window.list_layout[current_layout_pos]

            # Filter graph
            new_graph = copy.deepcopy(self.ui_window.graph_current)
            attribute_copy = [copy.deepcopy(a) for a in self.ui_window.list_attribute]
            for a in attribute_copy:
                a.filter_graph(new_graph)
            # We scale after filtering all element
            for a in attribute_copy:
                a.scale_graph(new_graph)

            side_fun.draw_graph(new_graph, current_layout)
            self.finished.emit()

    def runComputeAndDisplayGraph(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Ui_MainWindow.Graph_computer_worker(self)
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.display_graph)
        self.thread.finished.connect(self.thread.deleteLater)
        # Step 6: Start the thread
        self.thread.start()

        # Set build button to building
        self.layout_build_button.setText("Building")
        self.layout_build_button.setEnabled(False)

        self.attr_build_button.setText("Building")
        self.attr_build_button.setEnabled(False)

        self.edge_build_button.setText("Building")
        self.edge_build_button.setEnabled(False)

        self.node_build_button.setText("Building")
        self.node_build_button.setEnabled(False)

    def display_graph(self):
        self.webEngineView.load(
            QtCore.QUrl().fromLocalFile(str(pathlib.Path(pathlib.Path(__file__).parent.resolve()) / r"nx.html")))

        # Set build button back to build
        self.layout_build_button.setText("Build")
        self.layout_build_button.setEnabled(True)

        self.attr_build_button.setText("Build")
        self.attr_build_button.setEnabled(True)

        self.edge_build_button.setText("Build")
        self.edge_build_button.setEnabled(True)

        self.node_build_button.setText("Build")
        self.node_build_button.setEnabled(True)

    def on_tab_clicked(self, index):
        if index == 0:
            self.layout_selection_list_on_item_click(self.layout_selection_list.currentRow())
        elif index == 1:
            self.attr_selection_list_on_item_click(self.attr_selection_list.currentItem())
        elif index == 2:
            self.node_selection_list_on_item_click(self.node_selection_list.currentItem())
        elif index == 3:
            self.edge_selection_list_on_item_click(self.edge_selection_list.currentItem())

    def layout_selection_list_init(self):
        for l in self.list_layout:
            self.layout_selection_list.addItem(l.name)

        default_value = 0
        self.layout_selection_list.setCurrentRow(default_value)
        self.layout_selection_list_on_item_click(default_value)

    def layout_selection_list_update(self):
        self.layout_selection_list.clear()
        for l in self.list_layout:
            self.layout_selection_list.addItem(l.name)

        default_value = 0
        self.layout_selection_list.setCurrentRow(default_value)
        self.layout_selection_list_on_item_click(default_value)

    @staticmethod
    def layout_parameter_value_on_click_factory(layout_param):
        def layout_parameter_value_on_click(value):
            layout_param.start = value

        return layout_parameter_value_on_click

    @staticmethod
    def layout_parameter_boolean_on_click_factory(layout_param):
        def layout_parameter_boolean_on_click(boolean):
            layout_param.coched = boolean

        return layout_parameter_boolean_on_click

    @staticmethod
    def layout_parameter_categorical_on_click_factory(layout_param):
        def layout_parameter_categorical_on_click(pos):
            layout_param.start_choice_pos = pos

        return layout_parameter_categorical_on_click

    def layout_selection_list_on_item_click(self, item_row):
        self.layout_adaptive_display_clear()

        layout = self.list_layout[item_row]

        for p in layout.parameter_lst:
            mini_hlayout = QtWidgets.QHBoxLayout(self.tab_layout)

            # Add name
            label = QtWidgets.QLabel(self.tab_layout)
            label.setObjectName("Label_{}".format(p.name))
            label.setText("{}: ".format(p.name))
            mini_hlayout.addWidget(label)

            # Layout_parameter_value
            if p.data_type == 0:
                spinbox = QtWidgets.QDoubleSpinBox(self.tab_layout)
                spinbox.setObjectName("Spinbox_{}".format(p.name))

                spinbox.setDecimals(compute_number_of_decimal(p.start))
                spinbox.setMaximum(p.maximum)
                spinbox.setMinimum(p.minimum)
                spinbox.setSingleStep(p.step)
                spinbox.setValue(p.start)

                spinbox.valueChanged.connect(Ui_MainWindow.layout_parameter_value_on_click_factory(p))
                mini_hlayout.addWidget(spinbox)

            # Layout_parameter_boolean
            elif p.data_type == 1:
                checkbox = QtWidgets.QCheckBox(self.tab_layout)
                checkbox.setObjectName("Checkbox_{}".format(p.name))
                checkbox.setChecked(p.coched)
                checkbox.clicked.connect(Ui_MainWindow.layout_parameter_boolean_on_click_factory(p))
                mini_hlayout.addWidget(checkbox)

            # Layout_parameter_categorical
            elif p.data_type == 2:
                combobox = QtWidgets.QComboBox(self.tab_layout)
                combobox.setObjectName("ComboBox_{}".format(p.name))
                for choice in p.list_choice:
                    combobox.addItem(choice)
                combobox.setCurrentIndex(p.start_choice_pos)
                combobox.currentIndexChanged.connect(Ui_MainWindow.layout_parameter_categorical_on_click_factory(p))
                mini_hlayout.addWidget(combobox)

            else:
                raise Exception("ERROR: INVALID LAYOUT PARAMETER")

            # Add spacer to stick widget to the left
            spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            mini_hlayout.addSpacerItem(spacer)

            self.layout_layout_right.addLayout(mini_hlayout)
            self.layout_layout_right_widget_lst.append(mini_hlayout)

    def layout_adaptive_display_clear(self):
        for w in self.layout_layout_right_widget_lst:
            for i in reversed(range(w.count())):
                to_remove = w.itemAt(i).widget()
                w.removeWidget(to_remove)

            self.layout_layout_right.removeItem(w)

        self.layout_layout_right_widget_lst = []

    def attr_selection_list_init(self):
        for a in self.list_attribute:
            self.attr_selection_list.addItem(a.name)

        self.attr_selection_list.setCurrentRow(0)
        self.attr_selection_list_on_item_click(self.attr_selection_list.currentItem())

    def attr_selection_list_update(self):
        self.attr_selection_list.clear()
        for a in self.list_attribute:
            self.attr_selection_list.addItem(a.name)

        self.attr_selection_list.setCurrentRow(0)
        self.attr_selection_list_on_item_click(self.attr_selection_list.currentItem())

    @staticmethod
    def attr_numerical_scale_click_factory(attribute):
        def attr_numerical_scale_click(bool):
            attribute.scale_with_size = bool

        return attr_numerical_scale_click

    @staticmethod
    def attr_numerical_on_slider_click_factory(attribute):
        def attr_numerical_on_slider_click(tuple_min_max):
            attribute.current_min_value = tuple_min_max[0]
            attribute.current_max_value = tuple_min_max[1]

        return attr_numerical_on_slider_click

    @staticmethod
    def attrib_cat_boolean_on_click_factory(attrib_cat, i):
        def attrib_cat_boolean_on_click(boolean):
            attrib_cat.categories_to_keep[i] = boolean

        return attrib_cat_boolean_on_click

    @staticmethod
    def attrib_cat_color_on_click_factory(attrib_cat, i, qbutton):
        def attrib_cat_color_on_click():
            color = QColorDialog.getColor()
            if color.isValid():
                attrib_cat.categories_color[i] = color.name()
                qbutton.setStyleSheet("background-color: {}; border:  none".format(color.name()))

        return attrib_cat_color_on_click

    @staticmethod
    def attr_cat_apply_color_factory(attr, graph):
        def attr_cat_apply_color():
            for i in range(len(attr.categories)):
                color = attr.categories_color[i]
                if attr.categories_to_keep[i]:
                    if attr.related_to_node:
                        for n in attr.categories[i]:
                            side_fun.change_node_color(graph, n, color)
                    else:
                        for a, b in attr.categories[i]:
                            side_fun.change_edge_color(graph, a, b, color)

        return attr_cat_apply_color

    @staticmethod
    def attrib_num_color_on_click_factory(attrib_num, i, qbutton):
        def attrib_num_color_on_click():
            color = QColorDialog.getColor()
            if color.isValid():
                attrib_num.colors[i] = color.name()
                qbutton.setStyleSheet("background-color: {}; border:  none".format(color.name()))

        return attrib_num_color_on_click

    @staticmethod
    def attr_num_apply_color_factory(attr, graph):
        def attr_num_apply_color():
            attr.set_filtered_min_max()
            if attr.related_to_node:
                for n in graph.nodes:
                    if attr.current_min_value <= attr.values[n] <= attr.current_max_value:
                        color = attr.colors[attr.get_color_index(attr.values[n])]
                        side_fun.change_node_color(graph, n, color)
            else:
                for a, b in graph.edges:
                    if attr.current_min_value <= attr.values[a][b] <= attr.current_max_value:
                        color = attr.colors[attr.get_color_index(attr.values[a][b])]
                        side_fun.change_edge_color(graph, a, b, color)

        return attr_num_apply_color

    def attr_selection_list_on_item_click(self, item):
        self.reset_attrib_layout()
        # Disconnect if possible

        for w in [self.attr_filter_range_slider, self.attr_scale_with_size_checkbox, self.attr_apply_color_button]:
            try:
                while True:
                    w.disconnect()
            except TypeError: pass


        # Find attribute
        attribute = None
        for attribute in self.list_attribute:
            if attribute.name == item.text():
                break

        attribute.init_attr(self.graph_current)

        if attribute.type == 0:
            if (attribute.absolute_max_value - attribute.absolute_min_value) <= 0 or (
                    attribute.current_max_value - attribute.current_min_value) <= 0:
                self.attr_filter_range_slider.setVisible(False)
            else:
                self.set_attrib_layout_numerical(attribute)
                self.attr_filter_range_slider.setDecimals(attribute.n_decimals)
                self.attr_filter_range_slider.setVisible(True)

                self.attr_filter_range_slider.setMinimum(sys.float_info.min)
                self.attr_filter_range_slider.setMaximum(sys.float_info.max)
                self.attr_filter_range_slider.setMaximum(float(attribute.absolute_max_value))
                self.attr_filter_range_slider.setMinimum(float(attribute.absolute_min_value))

                self.attr_filter_range_slider.setValue((attribute.current_min_value, attribute.current_max_value))
                self.attr_filter_range_slider.valueChanged.connect(
                    Ui_MainWindow.attr_numerical_on_slider_click_factory(attribute))
                self.attr_scale_with_size_checkbox.setChecked(attribute.scale_with_size)
                self.attr_scale_with_size_checkbox.clicked.connect(
                    Ui_MainWindow.attr_numerical_scale_click_factory(attribute))
                self.attr_apply_color_button.clicked.connect(
                    Ui_MainWindow.attr_num_apply_color_factory(attribute, self.graph_current))

        elif attribute.type == 1:
            self.set_attrib_layout_categorical(attribute)
            self.attr_apply_color_button.clicked.connect(
                Ui_MainWindow.attr_cat_apply_color_factory(attribute, self.graph_current))

        attribute.is_init = True

    def reset_attrib_layout(self):
        self.attr_filter_range_slider.setVisible(False)
        self.attr_filter_label.setVisible(False)
        self.attr_scale_with_size_checkbox.setVisible(False)
        self.attr_scroll_area.setVisible(False)

        # Reset attrib layout
        for w in self.attr_cat_layout_widget_lst:
            for i in reversed(range(w.count())):
                to_remove = w.itemAt(i).widget()
                w.removeWidget(to_remove)
                to_remove.deleteLater()

            self.attr_cat_layout.removeItem(w)
        self.attr_cat_layout_widget_lst = []

        # Reset num layout
        for i in reversed(range(self.attr_num_color_hlayout.count())):
            to_remove = self.attr_num_color_hlayout.itemAt(i).widget()
            self.attr_num_color_hlayout.removeWidget(to_remove)
            to_remove.deleteLater()

    def set_attrib_layout_numerical(self, attrib):
        self.attr_filter_range_slider.setVisible(True)
        self.attr_filter_label.setVisible(True)
        self.attr_scale_with_size_checkbox.setVisible(True)

        for i in range(len(attrib.colors)):
            color_button = QtWidgets.QPushButton(self.tab_attr)
            color_button.setFlat(True)
            color_button.setText(" ")
            color_button.setStyleSheet("background-color: {}; border:  none".format(attrib.colors[i]))
            color_button.clicked.connect(Ui_MainWindow.attrib_num_color_on_click_factory(attrib, i, color_button))
            self.attr_num_color_hlayout.addWidget(color_button)

    def set_attrib_layout_categorical(self, attrib):
        self.attr_scroll_area.setVisible(True)

        for i in range(len(attrib.categories)):
            mini_hlayout = QtWidgets.QHBoxLayout()

            label = QtWidgets.QLabel(self.tab_attr)
            label.setObjectName("Label_{}".format(attrib.categories_name[i]))
            label.setText("{} ".format(attrib.categories_name[i]))
            mini_hlayout.addWidget(label, 50)

            checkbox = QtWidgets.QCheckBox(self.tab_attr)
            checkbox.setObjectName("Checkbox_{}".format(attrib.categories_name[i]))
            checkbox.setChecked(attrib.categories_to_keep[i])
            checkbox.clicked.connect(Ui_MainWindow.attrib_cat_boolean_on_click_factory(attrib, i))
            mini_hlayout.addWidget(checkbox, 10)

            color_button = QtWidgets.QPushButton(self.tab_attr)
            color_button.setObjectName("color_button{}".format(attrib.categories_name[i]))
            color_button.setFlat(True)
            color_button.setText(" ")
            color_button.setStyleSheet("background-color: {}; border:  none".format(attrib.categories_color[i]))
            color_button.clicked.connect(Ui_MainWindow.attrib_cat_color_on_click_factory(attrib, i, color_button))
            mini_hlayout.addWidget(color_button, 20)

            self.attr_cat_layout.addLayout(mini_hlayout)
            self.attr_cat_layout_widget_lst.append(mini_hlayout)

    def node_selection_list_init(self):
        self.all_nodes_size = 10
        self.all_nodes_color = "#ddc1ff"
        side_fun.change_all_node_size(self.graph_current, self.all_nodes_size)
        side_fun.change_all_node_color(self.graph_current, self.all_nodes_color)

        self.node_size_spinbox.setMinimum(1)
        self.node_size_spinbox.setMaximum(100000)
        self.node_size_spinbox.setDecimals(1)

        self.node_selection_list_update()

        self.node_selection_list.setCurrentRow(0)
        self.node_selection_list_on_item_click(self.node_selection_list.currentItem())

    def node_selection_list_update(self):
        self.node_selection_list.clear()
        self.node_selection_list.addItem(STR_ALL_NODES)
        for n in self.graph_current.nodes:
            self.node_selection_list.addItem(str(n))
        self.node_selection_list.sortItems()
        self.node_selection_list.setCurrentRow(0)

    def node_delete_from_list(self, item):
        side_fun.remove_Node(self.graph_current, int(item.text()))
        self.node_selection_list_update()

    @staticmethod
    def node_change_size_on_click_factory(graph_save, node_id):
        def node_change_size_on_click(size):
            side_fun.change_node_size(graph_save, node_id, size)

        return node_change_size_on_click

    @staticmethod
    def node_change_all_size_on_click_factory(ui_window):
        def node_change_all_size_on_click(size):
            ui_window.all_nodes_size = size
            side_fun.change_all_node_size(ui_window.graph_current, size)

        return node_change_all_size_on_click

    @staticmethod
    def node_change_color_on_click_factory(ui_window, node_id):
        def node_change_color_on_click():
            color = QColorDialog.getColor()
            if color.isValid():
                ui_window.tab_node_color_button.setStyleSheet(
                    "background-color: {}; border:  none".format(color.name()))
                side_fun.change_node_color(ui_window.graph_current, node_id, color.name())

        return node_change_color_on_click

    def node_change_all_color_on_click(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.all_nodes_color = color.name()
            self.tab_node_color_button.setStyleSheet("background-color: {}; border:  none".format(color.name()))
            side_fun.change_all_node_color(self.graph_current, color.name())

    def color_shortest_path_factory(self, source, graph, method='dijkstra'):
        def color_shortest_path_factory():
            target = int(self.node_shortest_path_to_combo.currentText())

            color = side_fun.get_node_color(graph, source)
            new_edge_size = self.all_edges_size * 2

            try:
                path = nx.algorithms.shortest_path(graph, source=source, target=target, method=method)
            except Exception as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Shortest path")
                msg.addButton(QtWidgets.QMessageBox.Close)
                msg.setText(str(e))
                msg.exec_()
                return
            idx = 0
            for i in range(len(path) - 1):
                side_fun.change_node_color(graph, path[idx], color)
                idx += 1
                side_fun.change_edge_color(graph, path[i], path[i + 1], color)
                side_fun.change_edge_width(graph, path[i], path[i+1], new_edge_size)
            side_fun.change_node_color(graph, path[idx], color)

        return color_shortest_path_factory

    def node_selection_list_on_item_click(self, item):
        try:
            self.node_size_spinbox.disconnect()
            self.tab_node_color_button.disconnect()
            self.node_shortest_path_button.disconnect()
        except TypeError: pass

        if item.text() == STR_ALL_NODES:
            self.node_size_spinbox.setValue(self.all_nodes_size)

            self.node_size_spinbox.valueChanged.connect(Ui_MainWindow.node_change_all_size_on_click_factory(self))
            self.tab_node_color_button.clicked.connect(self.node_change_all_color_on_click)
            self.tab_node_color_button.setStyleSheet("background-color: {}; border:  none".format(self.all_nodes_color))

            self.node_shortest_path_label.setVisible(False)
            self.node_shortest_path_to_combo.setVisible(False)
            self.node_shortest_path_button.setVisible(False)

        else:
            node_id = int(item.text())
            self.node_size_spinbox.setValue(side_fun.get_node_size(self.graph_current, node_id))
            current_color = side_fun.get_node_color(self.graph_current, node_id)

            self.node_size_spinbox.valueChanged.connect(
                Ui_MainWindow.node_change_size_on_click_factory(self.graph_current, node_id))
            self.tab_node_color_button.clicked.connect(self.node_change_color_on_click_factory(self, node_id))
            self.tab_node_color_button.setStyleSheet("background-color: {}; border:  none".format(current_color))

            self.node_shortest_path_label.setVisible(True)
            self.node_shortest_path_to_combo.setVisible(True)
            self.node_shortest_path_button.setVisible(True)
            node_to_lst = []
            for n in self.graph_current.nodes:
                if n != node_id: node_to_lst.append(str(n))
            self.node_shortest_path_to_combo.clear()
            self.node_shortest_path_to_combo.addItems(node_to_lst)

            self.node_shortest_path_button.clicked.connect(self.color_shortest_path_factory(node_id, self.graph_current))

    def node_selection_list_on_item_double_click(self, item):
        self.item = item
        if self.item.text() == STR_ALL_NODES:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Node data")
            msg.addButton(QtWidgets.QMessageBox.Close)
            msg.setText("APPLY TO ALL NODES")
            msg.exec_()
        else:
            self.data1 = self.df_node.loc[self.df_node['#BIOGRID ID'] == int(item.text())]
            self.data2 = self.df_chemicals.loc[self.df_chemicals['BioGRID Gene ID'] == int(item.text())]
            self.data3 = self.df_ptm.loc[self.df_ptm['BioGRID ID'] == int(item.text())]
            self.data4 = ""
            for attribute in self.list_attribute:
                if attribute.is_init:
                    self.data4 += f"<strong>{attribute.name}:</strong> "
                    if attribute.type == 0: #Numerical
                        inter = attribute.values.get(int(item.text()),-1)
                        if inter != -1:
                            self.data4 += f"{inter}<br>"
                    elif attribute.type == 1: #Categorical
                        index = -1
                        for i in range(len(attribute.categories)):
                            for j in range(len(attribute.categories[i])):
                                if attribute.categories[i][j] == int(item.text()):
                                    index = i
                                    break
                        if index != -1:
                            self.data4 += f"{attribute.categories_name[index]}<br>"

            tab_dialog = TabDialog(self)
            tab_dialog.exec_()

    def edge_selection_list_init(self):
        self.all_edges_size = 1
        self.all_edges_color = "#d7d7d7"
        side_fun.change_all_edge_width(self.graph_current, self.all_edges_size)
        side_fun.change_all_edge_color(self.graph_current, self.all_edges_color)

        self.edge_size_spinbox.setMinimum(0)
        self.edge_size_spinbox.setMaximum(100000)
        self.edge_size_spinbox.setDecimals(1)

        self.edge_selection_list_update()

        self.edge_selection_list.setCurrentRow(0)
        self.edge_selection_list_on_item_click(self.edge_selection_list.currentItem())

    def edge_selection_list_update(self):
        self.edge_selection_list.clear()
        self.edge_selection_list.addItem(STR_ALL_EDGES)

        for e in self.graph_current.edges:
            self.edge_selection_list.addItem(str(e))

        self.edge_selection_list.setCurrentRow(0)

    @staticmethod
    def edge_change_size_on_click_factory(graph_save, node_id1, node_id2):
        def edge_change_size_on_click(size):
            side_fun.change_edge_width(graph_save, node_id1, node_id2, size)

        return edge_change_size_on_click

    @staticmethod
    def edge_change_all_size_on_click_factory(ui_window):
        def edge_change_all_size_on_click(size):
            ui_window.all_edges_size = size
            side_fun.change_all_edge_width(ui_window.graph_current, size)

        return edge_change_all_size_on_click

    @staticmethod
    def edge_change_color_on_click_factory(ui_window, node_id1, node_id2):
        def edge_change_color_on_click():
            color = QColorDialog.getColor()
            if color.isValid():
                ui_window.tab_edge_color_button.setStyleSheet(
                    "background-color: {}; border:  none".format(color.name()))
                side_fun.change_edge_color(ui_window.graph_current, node_id1, node_id2, color.name())

        return edge_change_color_on_click

    def edge_change_all_color_on_click(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.all_edges_color = color.name()
            self.tab_edge_color_button.setStyleSheet("background-color: {}; border:  none".format(color.name()))
            side_fun.change_all_edge_color(self.graph_current, color.name())

    def edge_selection_list_on_item_click(self, item):
        self.edge_size_spinbox.disconnect()
        self.tab_edge_color_button.disconnect()

        if item.text() == STR_ALL_EDGES:
            self.edge_size_spinbox.setValue(self.all_edges_size)
            self.tab_edge_color_button.setStyleSheet("background-color: {}; border:  none".format(self.all_edges_color))

            self.edge_size_spinbox.valueChanged.connect(Ui_MainWindow.edge_change_all_size_on_click_factory(self))
            self.tab_edge_color_button.clicked.connect(self.edge_change_all_color_on_click)

        else:
            node1, node2 = side_fun.str_tuple_2_tuple(item.text())
            self.edge_size_spinbox.setValue(side_fun.get_edge_width(self.graph_current, node1, node2))
            current_color = side_fun.get_edge_color(self.graph_current, node1, node2)
            self.tab_edge_color_button.setStyleSheet("background-color: {}; border:  none".format(current_color))

            self.edge_size_spinbox.valueChanged.connect(
                Ui_MainWindow.edge_change_size_on_click_factory(self.graph_current, node1, node2))
            self.tab_edge_color_button.clicked.connect(self.edge_change_color_on_click_factory(self, node1, node2))

    def edge_selection_list_on_item_double_click(self, item):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Edge data")
        msg.addButton(QtWidgets.QMessageBox.Close)
        if item.text() == STR_ALL_EDGES:
            msg.setText("APPLY TO ALL EDGES")
        else:
            msg.addButton('Delete edge', QtWidgets.QMessageBox.YesRole)
            edge = item.text().strip('()').replace(" ", "").split(',')
            data = self.df_edge.loc[(self.df_edge['BioGRID ID Interactor A'] == int(edge[0])) & (
                    self.df_edge['BioGRID ID Interactor B'] == int(edge[1]))]
            if data.empty:
                msg.setText("No information available")
            else:
                msg.setText(side_fun.display_data(data))
        retVal = msg.exec_()
        if retVal != QMessageBox.Close:
            edge = item.text().strip('()').replace(" ", "").split(',')
            side_fun.remove_Edge(self.graph_current, int(edge[0]), int(edge[1]))
            self.edge_selection_list_init()

    @staticmethod
    def selection_list_filter(selection_list, filtering_str):
        for i in range(selection_list.count()):
            item = selection_list.item(i)
            item.setHidden(filtering_str != item.text()[:len(filtering_str)])


class TabDialog(QtWidgets.QDialog):
    def __init__(self, parent, origin=None):
        super(TabDialog, self).__init__(origin)
        self.parent = parent
        self.tabWidget = QtWidgets.QTabWidget()
        self.tab1 = QtWidgets.QWidget()
        self.label1 = QtWidgets.QLabel(self.tab1)
        no_info_str = "<strong>No information available</strong>"
        if self.parent.data1.empty:
            self.label1.setText(no_info_str)
        else:
            self.label1.setText(side_fun.display_data(self.parent.data1))

        self.tab2 = QtWidgets.QWidget()
        self.label2 = QtWidgets.QLabel(self.tab2)
        if self.parent.data2.empty:
            self.label2.setText(no_info_str)
        else:
            self.label2.setText(side_fun.display_data(self.parent.data2))

        self.tab3 = QtWidgets.QWidget()
        self.label3 = QtWidgets.QLabel(self.tab3)
        if self.parent.data3.empty:
            self.label3.setText(no_info_str)
        else:
            self.label3.setText(side_fun.display_data(self.parent.data3))

        self.tab4 = QtWidgets.QWidget()
        self.label4 = QtWidgets.QLabel(self.tab4)
        self.label4.setText(self.parent.data4)

        self.tabWidget.addTab(self.tab1, 'General')
        self.tabWidget.addTab(self.tab2, 'Chemicals')
        self.tabWidget.addTab(self.tab3, 'PTM')
        self.tabWidget.addTab(self.tab4, 'Attributes')

        self.pushButton = QtWidgets.QPushButton('Delete node', self)
        self.pushButton.clicked.connect(self.on_click)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(self.tabWidget)
        self.mainLayout.addWidget(self.pushButton)
        self.setLayout(self.mainLayout)
        self.resize(500, 400)
        self.setWindowTitle("Nodes data")

    @pyqtSlot()
    def on_click(self):
        side_fun.remove_Node(self.parent.graph_current, int(self.parent.item.text()))
        self.parent.node_selection_list_update()
        self.close()


def compute_number_of_decimal(float):
    abs_start = abs(float)
    if abs_start >= 100:
        num_dec = 0
    elif abs_start == 0:
        num_dec = 2
    else:
        num_dec = 1
        while abs_start < 1:
            abs_start *= 10
            num_dec += 1

    return num_dec


#Extended ComboBox found on https://stackoverflow.com/questions/4827207/how-do-i-filter-the-pyqt-qcombobox-items-based-on-the-text-input
class ExtendedComboBox(QComboBox):
    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

        # add a filter model to filter matching items
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)


    # on selection of an item from the completer, select the corresponding item from combobox
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
            self.activated[str].emit(self.itemText(index))


    # on model change, update the models of the filter and completer as well
    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)


    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
