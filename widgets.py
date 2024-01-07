from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QLineEdit, \
    QFrame, QMessageBox, QFileDialog

from fca_algorithm.algorithm import demonstrate, get_solution
from fca_algorithm.kb import KnowledgeBase
from plot import plot_graph


class ProblemWidget(QWidget):
    def __init__(self, kb: KnowledgeBase = None, file_name: str = None):
        super().__init__()

        self.knowledge_base = kb
        self.demonstration_steps = []
        self.file_name = file_name

        self.label_file_name = QLabel(self)
        self.editor_rules = QTextEdit(self)
        self.editor_facts = QTextEdit(self)
        self.editor_query = QLineEdit(self)
        self.editor_demonstration = QTextEdit(self)
        self.button_plot = QPushButton("Plot", self)
        self.button_demonstrate = QPushButton("Demonstrate", self)
        self.button_save_demonstration = QPushButton("Save Demonstration", self)
        self.button_save_kb = QPushButton("Save Knowledgebase", self)
        self.button_exit = QPushButton("Close", self)

        editor_knoledgebase_layout = QVBoxLayout(self)
        editor_knoledgebase_layout.addWidget(QLabel("Rules"))
        editor_knoledgebase_layout.addWidget(self.editor_rules)
        editor_knoledgebase_layout.addWidget(QLabel("Facts"))
        editor_knoledgebase_layout.addWidget(self.editor_facts)
        editor_knoledgebase_layout.addWidget(QLabel("Query"))
        editor_knoledgebase_layout.addWidget(self.editor_query)

        editor_Knoledgebase = QWidget()
        editor_Knoledgebase.setLayout(editor_knoledgebase_layout)

        grid_layout = QGridLayout()
        grid_layout.addWidget(QLabel("Knowledge Base"), 0, 0)
        grid_layout.addWidget(editor_Knoledgebase, 1, 0)
        grid_layout.addWidget(QLabel("Demonstration Steps"), 0, 1)
        grid_layout.addWidget(self.editor_demonstration, 1, 1)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.button_save_kb, alignment=Qt.AlignRight)
        button_layout.addWidget(self.button_demonstrate, alignment=Qt.AlignRight)
        button_layout.addWidget(self.button_save_demonstration, alignment=Qt.AlignRight)
        button_layout.addWidget(self.button_plot, alignment=Qt.AlignRight)
        button_layout.addWidget(self.button_exit, alignment=Qt.AlignRight)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label_file_name)
        main_layout.addWidget(get_separator())
        main_layout.addLayout(grid_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(get_separator())

        self.setLayout(main_layout)
        if self.knowledge_base:
            self.set_knowledge_base_editors()
        self.set_label_file_name()

        self.button_demonstrate.clicked.connect(self.demonstrate)
        self.button_exit.clicked.connect(self.close_window)
        self.button_save_demonstration.clicked.connect(self.save_demonstration)
        self.button_save_kb.clicked.connect(self.save_knowledge_base)
        self.button_plot.clicked.connect(self.plot)

    def close_window(self):
        self.close()

    def save_demonstration(self):
        if not self.file_name:
            return

        text = self.editor_demonstration.toPlainText()
        if text == '':
            QMessageBox.warning(self, 'Error', 'No demonstration to save')
            return

        file_name = self.file_name.split('.')[0] + '_demonstration.txt'
        file_to_save, _ = QFileDialog.getSaveFileName(self, 'Save Demonstration', file_name,
                                                      'Text Files (*.txt);;All Files (*)')
        if file_to_save:
            try:
                with open(file_to_save, 'w') as file:
                    file.write(text)
                QMessageBox.information(self, 'Success', 'Demonstration saved successfully')
            except Exception as e:
                QMessageBox.warning(self, 'Error', str(e))

    def save_knowledge_base(self):
        file_name = self.file_name if self.file_name else 'kb.kb'

        file_to_save, _ = QFileDialog.getSaveFileName(self, 'Save Knowledge Base', file_name,
                                                      'Knowledge Base Files (*.kb);;All Files (*)')
        if file_to_save:
            try:
                with open(file_to_save, 'w') as file:
                    file.write('\n'.join(self.get_kb_lines()))

                if not self.file_name:
                    self.file_name = file_to_save
                    self.set_label_file_name()
                QMessageBox.information(self, 'Success', 'Knowledge Base saved successfully')
            except Exception as e:
                QMessageBox.critical(self, 'Error', str(e))

    def demonstrate(self):
        if not self.set_knowledge_base():
            return

        status, steps = demonstrate(self.knowledge_base)
        if not status:
            self.editor_demonstration.setText('No solution found')
        else:
            self.demonstration_steps = get_solution(steps)
            self.editor_demonstration.setText(
                '\n'.join(str(step[0]) + ' -> ' + str(step[1]) for step in self.demonstration_steps))

    def plot(self):
        if not self.demonstration_steps:
            QMessageBox.warning(self, 'Error', 'Not demonstrated yet')
            return
        try:
            plot_graph(self.file_name, self.demonstration_steps)
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def set_knowledge_base(self):
        try:
            self.knowledge_base = KnowledgeBase(self.get_kb_lines())
            return True
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))
            return False

    def set_knowledge_base_editors(self):
        self.editor_rules.setText(self.knowledge_base.get_rules_as_string())
        self.editor_facts.setText(self.knowledge_base.get_facts_as_string())
        self.editor_query.setText(self.knowledge_base.get_query_as_string())

    def get_kb_lines(self):
        lines = ["kb:"]
        lines.extend(self.editor_rules.toPlainText().split('\n'))
        lines.extend(self.editor_facts.toPlainText().split('\n'))
        lines.append("query:")
        lines.append(self.editor_query.text())
        return lines

    def set_label_file_name(self):
        if self.file_name:
            self.label_file_name.setText(self.file_name)


def get_separator() -> QFrame:
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    return line
