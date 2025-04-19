import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem
from py_main import Ui_MainWindow
from  py_addEditCoffeeForm import Ui_addWindow

class AddEditCoffe(QMainWindow, Ui_addWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connection = sqlite3.connect("data\\coffee.db")
        self.id = -1
        self.status = 'add'
        self.resButton.clicked.connect(lambda: self.change_data(self.status))

    def closeEvent(self, event):
        self.id = -1
        self.close()
        ex.show()
        print(self.id)

    def change_data(self, prop='add'):
        cur = self.connection.cursor()
        if prop == 'add':
            cur.execute("""INSERT 
                        INTO main(name, roasting, type, description, price, size) 
                        VALUES (?, ?, ?, ?, ?, ?)""", (self.LineEdit_name.text(), self.LineEdit_roasting.text(),
                                                       self.LineEdit_type.text(), self.LineEdit_description.text(),
                                                       float(self.LineEdit_price.text()),
                                                       int(self.LineEdit_size.text()))).fetchall()
        else:
            cur.execute("""
            UPDATE main
            SET name = ?, roasting = ?, type = ?, description = ?, price =? , size = ? 
            WHERE id = ?""", (
                self.LineEdit_name.text(), self.LineEdit_roasting.text(),
                self.LineEdit_type.text(), self.LineEdit_description.text(),
                float(self.LineEdit_price.text()),
                int(self.LineEdit_size.text()), self.id)
                        )

        self.connection.commit()
        self.close()
        self.id = -1
        ex.show()
        ex.select_data()


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connection = sqlite3.connect("data\\coffee.db")
        self.select_data()
        self.addButton.clicked.connect(lambda: self.addeditwin(property='add'))
        self.editButton.clicked.connect(lambda: self.addeditwin(property='edit'))
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

    def addeditwin(self, property='add'):
        self.newform.LineEdit_name.setText('')
        self.newform.LineEdit_roasting.setText('')
        self.newform.LineEdit_type.setText('')
        self.newform.LineEdit_description.setText('')
        self.newform.LineEdit_price.setText('')
        self.newform.LineEdit_size.setText('')
        self.newform.id = self.main_table.currentIndex().row()

        if property == 'add':
            self.newform.status = 'add'
            self.newform.resButton.setText('Добавить')
            self.hide()
            self.newform.show()
        else:
            self.newform.status = 'edit'
            if self.newform.id == -1:
                self.statusBar().showMessage(f'Не выбрана строка для редактирования')
            else:
                self.newform.id = self.main_table.model().index(self.newform.id, 0).data()
                self.newform.resButton.setText('Изменить')

                cur = self.connection.cursor()
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
                    WHERE ID = ?
                    """, (self.newform.id,)).fetchall()
                self.newform.LineEdit_name.setText(res[0][1])
                self.newform.LineEdit_roasting.setText(res[0][2]),
                self.newform.LineEdit_type.setText(res[0][3])
                self.newform.LineEdit_description.setText(res[0][4])
                self.newform.LineEdit_price.setText(str(res[0][5]))
                self.newform.LineEdit_size.setText(str(int(res[0][6])))
                self.hide()
                self.newform.show()

    def closeEvent(self, event):
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
