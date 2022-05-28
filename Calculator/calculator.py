import sys
import functools

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QVBoxLayout
from PyQt5.QtCore import Qt

from Calculation import Computation, Operations, Numbers
from Helpers import get_recursive_children

class ValueDisplay(QLineEdit):
    def __init__(self):
        super().__init__()


class Controls(QWidget):
    def __init__(self, display: QLineEdit):
        super().__init__()

        self.layout = QGridLayout()

        calc = Computation(display)

        operations = Operations()
        opcodes = [
            {'code': 'CE', 'op': operations.CE},
            {'code': 'C', 'op': operations.C},
            {'code': '<-', 'op': operations.erase},
            {'code': '=', 'op': operations.equals},
            {'code': '+', 'op': operations.add},
            {'code': '-', 'op': operations.subtract},
            {'code': '*', 'op': operations.multiply},
            {'code': '/', 'op': operations.divide},
        ]
        for i, opcode in enumerate(opcodes):
            button = QPushButton(opcode['code'])
            if opcode['code'] not in ['=', '<-', 'C', 'CE']:
                button.clicked.connect(functools.partial(calc.add_op, opcode['code'], opcode['op']()))
                # button.clicked.connect(lambda op=opcode['op']: print(op))
            elif opcode['code'] == '=':
                button.clicked.connect(calc.compute)
            elif opcode['code'] == '<-':
                button.clicked.connect(calc.back)
            elif opcode['code'] in ['C', 'CE']:
                button.clicked.connect(calc.erase)
            self.layout.addWidget(button, i//4, i%4)

        numbers = Numbers()
        values = [
            *[{'code': str(code), 'op': numbers.number(code, display)} for code in [7, 8, 9, 4, 5, 6, 1, 2, 3]],
            {'code': '(', 'op': operations.negate},
            {'code': '0', 'op': numbers.number(0, display)},
            {'code': '.', 'op': operations.decimal},
            {'code': ')', 'op': operations.negate},
        ]
        for i, value in enumerate(values):
            button = QPushButton(value['code'])
            button.clicked.connect(functools.partial(calc.add_num, value['code']))
            # button.clicked.connect(lambda op=value['op']: op)
            if value['code'] == ')':
                self.layout.addWidget(button, i//3 + 1, 3)
            else:
                self.layout.addWidget(button, i//3 + 2, i%3)

        self.setLayout(self.layout)


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        display = ValueDisplay()
        layout.addWidget(display)
        layout.addWidget(Controls(display))

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)

window = Calculator()
window.show()

app.exec()