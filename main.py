import sys
import time

from PyQt5 import uic
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog
from PyQt5.QtSql import *

from databaseutilits import Database, Person, Dish, Restaurant, Order, Relation


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
        self.name = None
        self.surname = None
        self.amount = 1
        self.check_text = ''
        self.bill_text = 'Сумма к оплате:\n'
        self.bill_count = 0
        self.amount = 1

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

        self.make_order.clicked.connect(self.cook_order)

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
        self.name, ok_pressed_name = QInputDialog.getText(self, 'Окно ввода', 'Введите имя')
        if ok_pressed_name:
            self.surname, ok_pressed_surname = QInputDialog.getText(self, 'Окно ввода', 'Введите фамилию')
            if ok_pressed_name and ok_pressed_surname:
                self.database.add_person(Person([0, self.name, self.surname]))
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
            self.make_order_func(sender)

    def cook_order(self):
        self.bar.start()
        for _ in range(10):
            self.go_home_2.setEnabled(False)
            time.sleep(1)
        self.ready.show()
        self.go_home_2.setEnabled(True)

    def make_order_func(self, dish):
        self.check_text += f'{dish} \n'
        self.check.setText(self.check_text)
        price = self.database.get_dish(dish)[2]
        self.bill_count += price
        self.bill.setText(f'{self.bill_text}{self.bill_count}р')
        self.add_order(dish)

    def add_order(self, dish):
        restaurant_id = self.database.get_restaurant(self.rest, True)[0]
        person_id = self.database.get_person(self.name, True)[0]
        order = Order([0, restaurant_id, person_id])
        self.database.add_order(order)
        self.add_relation(order, dish)

    def add_relation(self, order, dish):
        order_id = self.database.get_order(order.person_id, True)[0]
        dish_id = self.database.get_dish(dish, True)[0]
        relation = Relation([order_id, dish_id, self.amount])
        self.database.add_relation(relation)

    def update(self):
        self.check_text = ''
        self.bill_text = 'Сумма к оплате:\n'
        self.bill_count = 0
        self.bill.setText('')
        self.check.setText('')

    def dish_show(self):
        if self.rest == 'McDonald`s' and self.category == 'Бургер':
            self.position_1_pick.setText('Гамбургер')
            self.position_2_pick.setText('Чизбургер')
            self.position_3_pick.setText('Чикен Премьер')
            self.position_4_pick.setText('Биг Мак')
            self.position_5_pick.setText('Филе о Фиш')
            self.position_1_price.setText('50р')
            self.position_2_price.setText('60р')
            self.position_3_price.setText('80р')
            self.position_4_price.setText('100р')
            self.position_5_price.setText('80р')
        elif self.rest == 'McDonald`s' and self.category == 'Напиток':
            self.position_1_pick.setText('Пепси-Кола')
            self.position_2_pick.setText('7UP')
            self.position_3_pick.setText('Фанта')
            self.position_4_pick.setText('Яблочный сок')
            self.position_5_pick.setText('Апельсиновый сок')
            self.position_1_price.setText('70р')
            self.position_2_price.setText('70р')
            self.position_3_price.setText('70р')
            self.position_4_price.setText('75р')
            self.position_5_price.setText('75р')
        elif self.rest == 'McDonald`s' and self.category == 'Закуска':
            self.position_1_pick.setText('Картофель Фри')
            self.position_2_pick.setText('Наггетсы')
            self.position_3_pick.setText('Стрипсы')
            self.position_4_pick.setText('Креветки')
            self.position_5_pick.setText('Яблочные Дольки')
            self.position_1_price.setText('50р')
            self.position_2_price.setText('90р')
            self.position_3_price.setText('70р')
            self.position_4_price.setText('80р')
            self.position_5_price.setText('100р')
        elif self.rest == 'Burger King' and self.category == 'Бургер':
            self.position_1_pick.setText('Воппер')
            self.position_2_pick.setText('Лонг Чикен')
            self.position_3_pick.setText('СтейкХаус')
            self.position_4_pick.setText('Биг Кинг')
            self.position_5_pick.setText('Сырный Джо')
            self.position_1_price.setText('80р')
            self.position_2_price.setText('90р')
            self.position_3_price.setText('220р')
            self.position_4_price.setText('100р')
            self.position_5_price.setText('150р')
        elif self.rest == 'Burger King' and self.category == 'Напиток':
            self.position_1_pick.setText('Пепси-Кола')
            self.position_2_pick.setText('7UP')
            self.position_3_pick.setText('Фанта')
            self.position_4_pick.setText('Каппучино')
            self.position_5_pick.setText('Молочный коктейль')
            self.position_1_price.setText('70р')
            self.position_2_price.setText('70р')
            self.position_3_price.setText('70р')
            self.position_4_price.setText('90р')
            self.position_5_price.setText('100р')
        elif self.rest == 'Burger King' and self.category == 'Закуска':
            self.position_1_pick.setText('Луковые кольца')
            self.position_2_pick.setText('Картофель Фри')
            self.position_3_pick.setText('Наггетсы')
            self.position_4_pick.setText('Чикен Фри')
            self.position_5_pick.setText('King GO')
            self.position_1_price.setText('60р')
            self.position_2_price.setText('50р')
            self.position_3_price.setText('90р')
            self.position_4_price.setText('80р')
            self.position_5_price.setText('100р')
        elif self.rest == 'KFC' and self.category == 'Бургер':
            self.position_1_pick.setText('Шефбургер')
            self.position_2_pick.setText('Шефбургер Делюкс')
            self.position_3_pick.setText('Чизбургер')
            self.position_4_pick.setText('Зингер')
            self.position_5_pick.setText('Сандерс')
            self.position_1_price.setText('120р')
            self.position_2_price.setText('150р')
            self.position_3_price.setText('60р')
            self.position_4_price.setText('100р')
            self.position_5_price.setText('180р')
        elif self.rest == 'KFC' and self.category == 'Напиток':
            self.position_1_pick.setText('Кока-Кола')
            self.position_2_pick.setText('Спрайт')
            self.position_3_pick.setText('Фанта')
            self.position_4_pick.setText('Молочный коктейль')
            self.position_5_pick.setText('Мохито')
            self.position_1_price.setText('70р')
            self.position_2_price.setText('70р')
            self.position_3_price.setText('70р')
            self.position_4_price.setText('100р')
            self.position_5_price.setText('120р')
        elif self.rest == 'KFC' and self.category == 'Закуска':
            self.position_1_pick.setText('Острые крылья')
            self.position_2_pick.setText('Стрипсы')
            self.position_3_pick.setText('Сырные подушечки')
            self.position_4_pick.setText('Картофель Фри')
            self.position_5_pick.setText('Байтсы')
            self.position_1_price.setText('50р')
            self.position_2_price.setText('50р')
            self.position_3_price.setText('80р')
            self.position_4_price.setText('50р')
            self.position_5_price.setText('70р')

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
