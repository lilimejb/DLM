import sys
import time

from PyQt5 import uic
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog
from PyQt5.QtSql import *

from databaseutilits import Database, Person, Dish, Restaurant


class Bar(QThread):
    def __init__(self, parent):
        QThread.__init__(self, parent=parent)
        self.parent = parent

    def run(self):
        cooking_time = 0
        percent = 10 / 100
        self.parent.cooking = True
        while cooking_time < 10:
            cooking_time += 1
            self.parent.cooking_proc.setValue(int(cooking_time / percent))
            time.sleep(1)

    def stop(self):
        sys.exit()


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.stack.setCurrentIndex(0)

        # подключение базы данных
        self.database = Database('orders.db')

        self.rest = None
        self.category = None

        self.bar = Bar(self)
        self.ready.hide()

        # подключение функций

        # функции переключения между окнами
        self.go_home_1.clicked.connect(self.set_main)
        self.go_home_3.clicked.connect(self.set_main)
        self.go_home_2.clicked.connect(self.set_main)
        self.go_to_reg.clicked.connect(self.set_reg)
        self.make_order_button.clicked.connect(self.set_order)
        self.oreder_view.clicked.connect(self.set_order_view)

        self.reg_button.clicked.connect(self.register)
        self.show_person_info()

        self.rest_choose.currentTextChanged.connect(self.rest_chosen)
        self.category_choose.currentTextChanged.connect(self.category_chosen)

        self.position_1_pick.clicked.connect(self.pick)
        self.position_2_pick.clicked.connect(self.pick)
        self.position_3_pick.clicked.connect(self.pick)
        self.position_4_pick.clicked.connect(self.pick)
        self.position_5_pick.clicked.connect(self.pick)

        self.make_order.clicked.connect(self.make_order_func)

    def set_main(self):
        self.stack.setCurrentIndex(0)
        self.update()

    def set_reg(self):
        self.stack.setCurrentIndex(1)

    def set_order(self):
        self.stack.setCurrentIndex(2)

    def set_order_view(self):
        self.stack.setCurrentIndex(3)

    def register(self):
        name, ok_pressed_name = QInputDialog.getText(self, 'Окно ввода', 'Введите имя')
        if ok_pressed_name:
            surname, ok_pressed_surname = QInputDialog.getText(self, 'Окно ввода', 'Введите фамилию')
            if ok_pressed_name and ok_pressed_surname:
                self.database.add_person(Person([0, name, surname]))
                self.show_person_info()

    def show_person_info(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('orders.db')
        db.open()
        model = QSqlTableModel(self, db)
        model.setTable('Persons')
        model.select()
        self.person_info.setModel(model)

    def rest_chosen(self):
        sender = self.sender().currentText()
        self.rest = sender
        self.dish_show()

    def category_chosen(self):
        sender = self.sender().currentText()
        self.category = sender
        self.dish_show()

    def pick(self):
        sender = self.sender().text()
        if sender == '':
            pass
        else:
            pass

    def make_order_func(self):
        self.bar.start()
        for _ in range(10):
            self.go_home_2.setEnabled(False)
            time.sleep(1)
        self.ready.show()
        self.go_home_2.setEnabled(True)

    def update(self):
        self.check.setText('')

    def dish_show(self):
        if self.rest == 'McDonald`s' and self.category == 'Бургер':
            self.position_1_pick.setText('Гамбургер (50р)')
            self.position_2_pick.setText('Чизбургер (60р)')
            self.position_3_pick.setText('Чикен Премьер (80р)')
            self.position_4_pick.setText('Биг Мак (100р)')
            self.position_5_pick.setText('Филе о Фиш (80р)')
        elif self.rest == 'McDonald`s' and self.category == 'Напиток':
            self.position_1_pick.setText('Пепси-Кола (70р)')
            self.position_2_pick.setText('7UP (70р)')
            self.position_3_pick.setText('Фанта (70р)')
            self.position_4_pick.setText('Яблочный сок (75р)')
            self.position_5_pick.setText('Апельсиновый сок (75р)')
        elif self.rest == 'McDonald`s' and self.category == 'Закуска':
            self.position_1_pick.setText('Картофель Фри (50р)')
            self.position_2_pick.setText('Наггетсы (90р)')
            self.position_3_pick.setText('Стрипсы (70р)')
            self.position_4_pick.setText('Креветки (80р)')
            self.position_5_pick.setText('Яблочные Дольки (100р)')
        elif self.rest == 'Burger King' and self.category == 'Бургер':
            self.position_1_pick.setText('Воппер (80р)')
            self.position_2_pick.setText('Лонг Чикен (90р)')
            self.position_3_pick.setText('СтейкХаус (220р)')
            self.position_4_pick.setText('Биг Кинг (100р)')
            self.position_5_pick.setText('Сырный Джо (150р)')
        elif self.rest == 'Burger King' and self.category == 'Напиток':
            self.position_1_pick.setText('Пепси-Кола (70р)')
            self.position_2_pick.setText('7UP (70р)')
            self.position_3_pick.setText('Фанта (70р)')
            self.position_4_pick.setText('Каппучино (90р)')
            self.position_5_pick.setText('Молочный коктейль (100р)')
        elif self.rest == 'Burger King' and self.category == 'Закуска':
            self.position_1_pick.setText('Луковые кольца (60р)')
            self.position_2_pick.setText('Картофель Фри (50р)')
            self.position_3_pick.setText('Наггетсы (90р)')
            self.position_4_pick.setText('Чикен Фри (80р)')
            self.position_5_pick.setText('King GO (100р)')
        elif self.rest == 'KFC' and self.category == 'Бургер':
            self.position_1_pick.setText('Шефбургер (120р)')
            self.position_2_pick.setText('Шефбургер Делюкс (150р)')
            self.position_3_pick.setText('Чизбургер (60р)')
            self.position_4_pick.setText('Зингер (100р)')
            self.position_5_pick.setText('Сандерс (180р)')
        elif self.rest == 'KFC' and self.category == 'Напиток':
            self.position_1_pick.setText('Кока-Кола (70р)')
            self.position_2_pick.setText('Спрайт (70р)')
            self.position_3_pick.setText('Фанта (70р)')
            self.position_4_pick.setText('Молочный коктель (100р)')
            self.position_5_pick.setText('Мохито (120р)')
        elif self.rest == 'KFC' and self.category == 'Закуска':
            self.position_1_pick.setText('Острые крылья (50р)')
            self.position_2_pick.setText('Стрипсы (50р)')
            self.position_3_pick.setText('Сырные подушечки (80р)')
            self.position_4_pick.setText('Картофель фри (50р)')
            self.position_5_pick.setText('Байтсы (70р)')

    def closeEvent(self, event):
        self.bar.stop()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWin()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
