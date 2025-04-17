import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem


class AddEditCoffe(QMainWindow):
    def __init__(self):
        super().__init__()
        self.connection = sqlite3.connect("coffee.db")
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.resButton.clicked.connect(lambda: self.add_new_data())

    def add_new_data(self):
        cur = self.connection.cursor()
        cur.execute(
            """INSERT 
            INTO main(name, roasting, type, description, price, size) 
            VALUES (?, ?, ?, ?, ?, ?)""", (self.LineEdit_name.text(), self.LineEdit_roasting.text(),
                                           self.LineEdit_type.text(), self.LineEdit_description.text(),
                                           float(self.LineEdit_price.text()),
                                           int(self.LineEdit_size.text()))).fetchall()
        self.connection.commit()
        self.close()
        ex.show()
        ex.select_data()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.connection = sqlite3.connect("coffee.db")
        uic.loadUi('main.ui', self)
        self.select_data()
        self.addButton.clicked.connect(lambda: self.addeditwin())
        self.editButton.clicked.connect(lambda: self.addeditwin('edit'))
        self.newform = AddEditCoffe()

    def select_data(self):
        cur = self.connection.cursor()
        cur.execute('PRAGMA table_info("main")')
        column_names = [i[1] for i in cur.fetchall()]
        res = cur.execute(
            """
            SELECT 
            id as ID, 
            name as Название,
            roasting as Обжарка,
            type as Типаж,
            description as Описание,
            price as Цена, 
            size as Вес
            FROM main
            ORDER BY ID
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
            self.statusBar().showMessage(f'В базе присутствует {len(res)} сортов кофе')
        else:
            self.statusBar().showMessage('К сожалению, база данных пуста')

    def addeditwin(self, par='add'):
        if par == 'add':
            self.newform.resButton.setText('Добавить')
        else:
            self.newform.resButton.setText('Изменить')
        self.hide()
        self.newform.show()

    def closeEvent(self, event):
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
