from PyQt5 import QtCore, QtGui, QtWidgets
import GraphX_MainWindow
from PyQt5.QtWidgets import QFileDialog, QDialog
import pathlib


class Ui_MainWindow(QDialog):
    DEFAULT_FILE_SELECTED_STRING = "File selected:"
    MAX_SIZE_FILE_DISPLAY = 45

    BUTTON_WIDTH_RATIO = 4
    LABEL_WIDTH_RATIO = 10 - BUTTON_WIDTH_RATIO

    def open_main(self):
        if (GraphX_MainWindow.FILE_NODES_PATH is None) or (GraphX_MainWindow.FILE_EDGES_PATH is None) or (GraphX_MainWindow.FILE_CHEMICALS_PATH is None) or (GraphX_MainWindow.FILE_PTM_PATH is None):
            return

        self.window = QtWidgets.QMainWindow()
        self.ui = GraphX_MainWindow.Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.retranslateUi(self.window)
        self.window.show()
        MainWindow.hide()

    def on_click_select_nodes_file(self):
        curr_dir = str(pathlib.Path(pathlib.Path(__file__).parent.resolve()))
        path = QFileDialog.getOpenFileName(self, "Select nodes .csv or .txt file", curr_dir,
                                           "CSV files (*.csv), TXT files (*.txt)")
        if path is None: return  # On cancel

        path = path[0]
        GraphX_MainWindow.FILE_NODES_PATH = path
        self.label.setText("{} {}".format(self.DEFAULT_FILE_SELECTED_STRING, path[:self.MAX_SIZE_FILE_DISPLAY]))

    def on_click_select_edges_file(self):
        curr_dir = str(pathlib.Path(pathlib.Path(__file__).parent.resolve()))
        path = QFileDialog.getOpenFileName(self, "Select edges .csv or .txt file", curr_dir,
                                           "CSV files (*.csv), TXT files (*.txt)")
        if path is None: return  # On cancel

        path = path[0]
        GraphX_MainWindow.FILE_EDGES_PATH = path
        self.label_2.setText("{} {}".format(self.DEFAULT_FILE_SELECTED_STRING, path[:self.MAX_SIZE_FILE_DISPLAY]))

    def on_click_select_chemicals_file(self):
        curr_dir = str(pathlib.Path(pathlib.Path(__file__).parent.resolve()))
        path = QFileDialog.getOpenFileName(self, "Select nodes .csv or .txt file", curr_dir,
                                           "CSV files (*.csv), TXT files (*.txt)")
        if path is None: return  # On cancel

        path = path[0]
        GraphX_MainWindow.FILE_CHEMICALS_PATH = path
        self.label_3.setText("{} {}".format(self.DEFAULT_FILE_SELECTED_STRING, path[:self.MAX_SIZE_FILE_DISPLAY]))

    def on_click_select_ptm_file(self):
        curr_dir = str(pathlib.Path(pathlib.Path(__file__).parent.resolve()))
        path = QFileDialog.getOpenFileName(self, "Select nodes .csv or .txt file", curr_dir,
                                           "CSV files (*.csv), TXT files (*.txt)")
        if path is None: return  # On cancel

        path = path[0]
        GraphX_MainWindow.FILE_PTM_PATH = path
        self.label_4.setText("{} {}".format(self.DEFAULT_FILE_SELECTED_STRING, path[:self.MAX_SIZE_FILE_DISPLAY]))

    def setupUi(self, MainWindow):
        # Set default value
        GraphX_MainWindow.FILE_NODES_PATH = None
        GraphX_MainWindow.FILE_EDGES_PATH = None
        GraphX_MainWindow.FILE_CHEMICALS_PATH = None
        GraphX_MainWindow.FILE_PTM_PATH = None

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 610)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_label.sizePolicy().hasHeightForWidth())
        self.title_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.verticalLayout.addWidget(self.title_label)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.on_click_select_nodes_file)
        self.horizontalLayout_2.addWidget(self.pushButton_2, self.BUTTON_WIDTH_RATIO)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label, self.LABEL_WIDTH_RATIO)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.on_click_select_edges_file)
        self.horizontalLayout_3.addWidget(self.pushButton_3, self.BUTTON_WIDTH_RATIO)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.label_2.installEventFilter(self)
        self.horizontalLayout_3.addWidget(self.label_2, self.LABEL_WIDTH_RATIO)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem2)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.on_click_select_chemicals_file)
        self.horizontalLayout_4.addWidget(self.pushButton_4, self.BUTTON_WIDTH_RATIO)

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3, self.LABEL_WIDTH_RATIO)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem3)
        ###
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.on_click_select_ptm_file)
        self.horizontalLayout_5.addWidget(self.pushButton_5, self.BUTTON_WIDTH_RATIO)

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4, self.LABEL_WIDTH_RATIO)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.open_main)
        self.verticalLayout.addWidget(self.pushButton)

        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GraphX"))
        self.title_label.setText(_translate("MainWindow", "Welcome to GraphX"))
        self.pushButton_2.setText(_translate("MainWindow", "Select genes (nodes) file"))
        self.label.setText(_translate("MainWindow", self.DEFAULT_FILE_SELECTED_STRING))
        self.pushButton_3.setText(_translate("MainWindow", "Select interactions (edges) file"))
        self.label_2.setText(_translate("MainWindow", self.DEFAULT_FILE_SELECTED_STRING))
        self.pushButton_4.setText(_translate("MainWindow", "Select chemicals file"))
        self.label_3.setText(_translate("MainWindow", self.DEFAULT_FILE_SELECTED_STRING))
        self.pushButton_5.setText(_translate("MainWindow", "Select PTM file"))
        self.label_4.setText(_translate("MainWindow", self.DEFAULT_FILE_SELECTED_STRING))
        self.pushButton.setText(_translate("MainWindow", "Build graph"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
