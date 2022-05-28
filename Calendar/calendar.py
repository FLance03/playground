import sys

from PyQt5.QtWidgets import \
    (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QStackedLayout, QHBoxLayout, QSpinBox)
from PyQt5.QtCore import Qt

from CalendarPage.MonthlyCalendar import MonthlyCalendar
import WidgetManagement


class DisplayDate(QWidget):
    def __init__(self, month):
        super().__init__()

        layout = QVBoxLayout()
        label = QLabel(month + " 2020")
        layout.addWidget(label)
        self.setLayout(layout)


class Calendar(QMainWindow):
    def __init__(self):
        super().__init__()

        self.months_combo = QComboBox()
        self.months_combo.addItems(['January', 'February', 'March', 'April', 'May', 'June',
                               'July', 'August', 'September', 'October', 'November', 'December'])
        self.months_combo.currentIndexChanged.connect(self.change_month)

        year_spin = QSpinBox()
        year_spin.setMinimum(0)
        year_spin.setMaximum(2022)
        year_spin.setValue(2021)
        year_spin.valueChanged.connect(self.change_year)

        month_year = QHBoxLayout()
        month_year.addWidget(self.months_combo)
        month_year.addWidget(year_spin)

        self.month_pages = QStackedLayout()
        self.set_month_pages(year_spin.value())

        self.layout = QVBoxLayout()
        self.layout.addLayout(month_year)
        self.layout.addLayout(self.month_pages)

        widget = QWidget()
        widget.setLayout(self.layout)

        # self.resize(500, 500)
        self.setCentralWidget(widget)

    def change_month(self, month_num):
        self.month_pages.setCurrentIndex(month_num)

    def change_year(self, year_num):
        WidgetManagement.clear_layout(self.month_pages)
        self.set_month_pages(year_num)
        self.month_pages.setCurrentIndex(self.months_combo.currentIndex())

        self.layout.addLayout(self.month_pages)

    def set_month_pages(self, year_num):
        month_days = self.get_months_info(year_num)
        for month in month_days:
            self.month_pages.addWidget(MonthlyCalendar(month['num_days']))

    def get_months_info(self, year_num):
        return [{'month': 'January', 'num_days': 30},
                {'month': 'February', 'num_days': 29 if (year_num % 4 == 0 and
                                                         year_num % 100 != 0) or year_num % 400 == 0 else 28},
                {'month': 'March', 'num_days': 30},
                {'month': 'April', 'num_days': 30},
                {'month': 'May', 'num_days': 30},
                {'month': 'June', 'num_days': 30},
                {'month': 'July', 'num_days': 30},
                {'month': 'August', 'num_days': 30},
                {'month': 'September', 'num_days': 30},
                {'month': 'October', 'num_days': 30},
                {'month': 'November', 'num_days': 30},
                {'month': 'December', 'num_days': 30},
                ]


app = QApplication(sys.argv)
window = Calendar()
window.show()
app.exec()
