import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.connection = sqlite3.connect("coffee.db")
        uic.loadUi('main.ui', self)
        self.select_data()

    def select_data(self):
        cur = self.connection.cursor()
        cur.execute('PRAGMA table_info("main")')
        column_names = [i[1] for i in cur.fetchall()]
        res = cur.execute(
            """SELECT 
    id as ID, 
    name as Название,
    roasting as Обжарка,
    type as Типаж,
    description as Описание,
    price as Цена, 
    size as Вес
FROM main
ORDER BY Название
            """).fetchall()
        self.main_table.setColumnCount(len(column_names))
        self.main_table.setRowCount(0)
        self.main_table.setHorizontalHeaderLabels(column_names)

        for i, row in enumerate(res):
            self.main_table.setRowCount(
                self.main_table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.main_table.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        if res:
            self.statusBar().showMessage(f'Нашлось {len(res)} сортов кофе')
        else:
            self.statusBar().showMessage('К сожалению, база данных пуста')

    def closeEvent(self, event):
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
