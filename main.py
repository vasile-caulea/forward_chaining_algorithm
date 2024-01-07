import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QMessageBox, QFileDialog, QVBoxLayout, \
    QWidget, QScrollArea

import widgets
from fca_algorithm.kb import KnowledgeBase


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Forward Chaining Algorithm")
        self.setMinimumSize(800, 600)
        self.create_menu_bar()

        self.layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.central_widget)
        self.setCentralWidget(self.scroll_area)

    def create_menu_bar(self):
        self.create_file_menu()
        self.create_help_menu()

    def create_file_menu(self):
        new_file_action = QAction("&New", self)
        new_file_action.triggered.connect(self.new_file)

        open_files_action = QAction("&Load Knowledge Bases", self)
        open_files_action.triggered.connect(self.load_knowledge_bases)

        exit_action = QAction("&Exit", self)
        exit_action.triggered.connect(self.quit_application)

        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(new_file_action)
        file_menu.addAction(open_files_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

    def create_help_menu(self):

        about_action = QAction("&About", self)
        about_action.triggered.connect(self.about_application)

        help_menu = self.menuBar().addMenu("&Help")
        help_menu.addAction(about_action)

    def new_file(self):
        self.layout.addWidget(widgets.ProblemWidget())

    def load_knowledge_bases(self) -> None:
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_names, _ = QFileDialog.getOpenFileNames(self, "Load Knowledge Bases", "",
                                                     "Knowledge Base Files (*.kb);;All Files (*)", options=options)
        if file_names:
            self.__set_widgets(file_names)

    def about_application(self):
        QMessageBox.about(self, "About", "Forward Chaining Algorithm")

    def __set_widgets(self, file_names) -> None:
        for file in file_names:
            try:
                with open(file, 'r') as f:
                    kb = KnowledgeBase(f.readlines())
            except Exception as e:
                QMessageBox.critical(self, 'Error', str(e))
                kb = None
            edit_widget = widgets.ProblemWidget(kb, file)
            self.layout.addWidget(edit_widget)

    def quit_application(self) -> None:
        really_quit = QMessageBox.question(self, "Exit", "Are you sure you want to quit?",
                                           QMessageBox.Yes | QMessageBox.No)

        if really_quit == QMessageBox.Yes:
            self.close()

    def closeEvent(self, e: QtGui.QCloseEvent) -> None:
        really_quit = QMessageBox.question(self, "Exit", "Are you sure you want to quit?",
                                           QMessageBox.Yes | QMessageBox.No)
        if really_quit == QMessageBox.Yes:
            e.accept()
        else:
            e.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
