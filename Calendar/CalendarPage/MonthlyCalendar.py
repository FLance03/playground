from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame, QGridLayout
from PyQt5.QtGui import QPainterPath, QRegion, QPainter, QLinearGradient, QPalette, QColor, QCursor
from PyQt5.QtCore import Qt, QRectF


class DayBox(QWidget):
    def __init__(self, day: 'int'):
        super().__init__()

        # self.setFrameStyle(QFrame.Panel | QFrame.Plain)

        # self.setAutoFillBackground(True)
        # p = self.palette()
        # p.setColor(self.backgroundRole(), QColor('blue'))
        # self.setPalette(p)


        box_label = QLabel(str(day))
        box_label.setAlignment(Qt.AlignCenter)
        # box_label.setStyleSheet('background-color: lightgreen;')

        layout = QVBoxLayout()
        layout.addWidget(box_label)

        self.setLayout(layout)

    def resizeEvent(self, e):
        radius = 7.0
        path = QPainterPath()
        path.addRoundedRect(0.0, 0.0, self.width(), self.height(), radius, radius)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)

    def paintEvent(self, e):
        radius = 7.0
        painter = QPainter(self)
        painter.drawRoundedRect(1, 1, self.width() - 2, self.height() - 2, radius, radius)


class MonthlyCalendar(QWidget):
    def __init__(self, num_days):
        super().__init__()

        # self.setAutoFillBackground(True)
        # p = self.palette()
        # p.setColor(self.backgroundRole(), QColor('red'))
        # self.setPalette(p)

        layout = QGridLayout()
        for day in range(1, num_days + 1):
            day_box = DayBox(day)
            layout.addWidget(day_box, (day - 1)//10, (day - 1)%10)
        # layout.setSpacing(20)

        self.setLayout(layout)