import sys
import time

from PyQt5 import uic
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog
from PyQt5.QtSql import *

from databaseutilits import Database, Person, Order, Relation

BACKGROUND_STYLE1 = """background-color: #D7FDF0;"""
BACKGROUND_STYLE2 = """background-color: #E4DFDA;"""

STYLE1 = """
    *{
	    background:linear-gradient(to bottom, #62c1e0 5%, #019ad2 100%);
	    background-color:#B2FFD6;
	    border-radius:6px;
	    border:1px solid #057fd0;
	    color:#AA78A6;
	    font-family:Arial;
	    font-size:15px;
	    font-weight:bold;
	    padding:6px 6px;
	    text-decoration:none;
    }
        *:hover {
	    background:linear-gradient(to bottom, #019ad2 5%, #62c1e0 100%);
	    background-color:#B4D6D3;
    }
    *:active {
	    position:relative;
	    top:1px;
    }
"""

STYLE2 = """*{
	background:linear-gradient(to bottom, #62c1e0 5%, #019ad2 100%);
	background-color:#824670;
	border-radius:6px;
	border:1px solid #FFFFFF;
	color:#E4DFDA;
	font-family:Arial;
	font-size:15px;
	font-weight:bold;
	padding:6px 6px;
	text-decoration:none;
}
*:hover {
	background:linear-gradient(to bottom, #019AD2 5%, #62C1E0 100%);
	background-color:#BDA0BC;
}
*:active {
	position:relative;
	top:1px;
}
"""


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


class Registration_Error(TypeError):
    pass


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.stack.setCurrentIndex(0)

        # подключение базы данных
        self.database = Database('orders.db')

        # инициализация переменных для удобства
        self.rest = None
        self.category = None
        self.name = None
        self.surname = None
        self.order_id = 0
        self.order_id_current = None
        self.new_order_flag = True
        self.check_text = ''
        self.bill_text = 'Сумма к оплате:\n'
        self.bill_count = 0
        self.amount = 1

        # self.bar = Bar(self)
        # self.ready.hide()

        # подключение функций

        # функции переключения между окнами
        self.go_home_1.clicked.connect(self.set_main)
        self.go_home_3.clicked.connect(self.set_main)
        self.go_home_2.clicked.connect(self.set_main)
        self.go_to_reg.clicked.connect(self.set_reg)
        self.make_order_button.clicked.connect(self.set_order)
        self.oreder_view.clicked.connect(self.set_order_view)

        # функции для регестрации
        self.reg_button.clicked.connect(self.registration)
        self.show_person_info()

        # ComboBox для выбора ресторана и категории блюда
        self.rest_choose.currentTextChanged.connect(self.rest_chosen)
        self.category_choose.currentTextChanged.connect(self.category_chosen)

        # функция для отчистки чека
        self.clean_list.clicked.connect(self.new_order)

        # кнопки для выбора блюда
        self.position_1_pick.clicked.connect(self.pick)
        self.position_2_pick.clicked.connect(self.pick)
        self.position_3_pick.clicked.connect(self.pick)
        self.position_4_pick.clicked.connect(self.pick)
        self.position_5_pick.clicked.connect(self.pick)

        # кнопка для старта Progress bar
        # self.make_order.clicked.connect(self.cook_order)

        # подключение смены темы
        self.green.triggered.connect(self.change_theme)
        self.blue.triggered.connect(self.change_theme)

        self.create_order.clicked.connect(self.new_order)

    # функция для перехода на главное окно
    def set_main(self):
        self.stack.setCurrentIndex(0)
        self.update()

    # функция для перехода на окно регестрации
    def set_reg(self):
        self.stack.setCurrentIndex(1)

    # функция для перехода на окно оформления заказа
    def set_order(self):
        self.stack.setCurrentIndex(2)

    # функция для перехода на окно просмотра заказов
    def set_order_view(self):
        self.stack.setCurrentIndex(3)

    # функция для регестрации пользователя
    def registration(self):
        self.name, ok_pressed_name = QInputDialog.getText(self, 'Окно регистрации', 'Введите имя')
        if ok_pressed_name:
            self.surname, ok_pressed_surname = QInputDialog.getText(self, 'Окно ввода', 'Введите фамилию')
            if ok_pressed_name and ok_pressed_surname:
                self.database.add_person(Person([0, self.name, self.surname]))
                self.show_person_info()

    # функция для показа информации о пользователе
    def show_person_info(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('orders.db')
        db.open()
        model = QSqlTableModel(self, db)
        model.setTable('Persons')
        model.select()
        self.person_info.setModel(model)

    # функция выбора ресторана
    def rest_chosen(self):
        sender = self.sender().currentText()
        self.rest = sender
        self.dish_show()

    # функция выбора категории блюда
    def category_chosen(self):
        sender = self.sender().currentText()
        self.category = sender
        self.dish_show()

    # функция выбора блюда
    def pick(self):
        sender = self.sender().text()
        if sender == '':
            pass
        else:
            if sender == self.position_1_pick.text():
                self.make_order_func(sender, self.position_1_amount.text())
            elif sender == self.position_2_pick.text():
                self.make_order_func(sender, self.position_2_amount.text())
            elif sender == self.position_3_pick.text():
                self.make_order_func(sender, self.position_3_amount.text())
            elif sender == self.position_4_pick.text():
                self.make_order_func(sender, self.position_4_amount.text())
            elif sender == self.position_5_pick.text():
                self.make_order_func(sender, self.position_5_amount.text())

    # функция выбора ресторана
    def make_order_func(self, dish, amount):
        # current_amount = self.check.text().find(dish)
        # print(current_amount)
        if dish in self.check_text or amount == '0':
            pass
        else:
            self.check_text += f'{dish} x{amount} \n'
            self.check.setText(self.check_text)
            price = self.database.get_dish(dish)[2]
            self.bill_count += price * int(amount)
            self.bill.setText(f'{self.bill_text}{self.bill_count}р')
            self.order_id_current = self.order_id
            if self.new_order_flag:
                self.new_order_flag = False
                self.add_order(dish, amount)
            else:
                self.add_relation(dish, amount)

    # функция добавления заказа
    def add_order(self, dish, amount):
        restaurant_id = self.database.get_restaurant(self.rest, True)[0]
        person_id = self.database.get_person(self.name, True)[0]
        order = Order([self.order_id_current, restaurant_id, person_id])
        self.database.add_order(order)
        self.add_relation(dish, amount)

    # функция "связки" заказа и блюда
    def add_relation(self, dish, amount):
        # order_id = self.database.get_order(order.person_id, True)[0]
        dish_id = self.database.get_dish(dish, True)[0]
        relation = Relation([self.order_id_current, dish_id, amount])
        self.database.add_relation(relation)

    # смена темы
    def change_theme(self):
        sender = self.sender().text()
        if sender == 'Зелёная':
            self.go_home_1.setStyleSheet(STYLE1)
            self.go_home_3.setStyleSheet(STYLE1)
            self.go_home_2.setStyleSheet(STYLE1)
            self.go_to_reg.setStyleSheet(STYLE1)
            self.make_order_button.setStyleSheet(STYLE1)
            self.oreder_view.setStyleSheet(STYLE1)
            self.reg_button.setStyleSheet(STYLE1)
            self.rest_choose.setStyleSheet(STYLE1)
            self.category_choose.setStyleSheet(STYLE1)
            self.position_1_pick.setStyleSheet(STYLE1)
            self.position_2_pick.setStyleSheet(STYLE1)
            self.position_3_pick.setStyleSheet(STYLE1)
            self.position_4_pick.setStyleSheet(STYLE1)
            self.position_5_pick.setStyleSheet(STYLE1)
            self.make_order.setStyleSheet(STYLE1)
            self.clean_list.setStyleSheet(STYLE1)
            self.position_1_amount.setStyleSheet(STYLE1)
            self.position_2_amount.setStyleSheet(STYLE1)
            self.position_3_amount.setStyleSheet(STYLE1)
            self.position_4_amount.setStyleSheet(STYLE1)
            self.position_5_amount.setStyleSheet(STYLE1)
            self.setStyleSheet(BACKGROUND_STYLE1)
        elif sender == 'Синяя':
            self.go_home_1.setStyleSheet(STYLE2)
            self.go_home_3.setStyleSheet(STYLE2)
            self.go_home_2.setStyleSheet(STYLE2)
            self.go_to_reg.setStyleSheet(STYLE2)
            self.make_order_button.setStyleSheet(STYLE2)
            self.oreder_view.setStyleSheet(STYLE2)
            self.reg_button.setStyleSheet(STYLE2)
            self.rest_choose.setStyleSheet(STYLE2)
            self.category_choose.setStyleSheet(STYLE2)
            self.position_1_pick.setStyleSheet(STYLE2)
            self.position_2_pick.setStyleSheet(STYLE2)
            self.position_3_pick.setStyleSheet(STYLE2)
            self.position_4_pick.setStyleSheet(STYLE2)
            self.position_5_pick.setStyleSheet(STYLE2)
            self.make_order.setStyleSheet(STYLE2)
            self.clean_list.setStyleSheet(STYLE2)
            self.position_1_amount.setStyleSheet(STYLE2)
            self.position_2_amount.setStyleSheet(STYLE2)
            self.position_3_amount.setStyleSheet(STYLE2)
            self.position_4_amount.setStyleSheet(STYLE2)
            self.position_5_amount.setStyleSheet(STYLE2)
            self.setStyleSheet(BACKGROUND_STYLE2)

    # функция отчистки всех переменных
    def update(self):
        self.check_text = ''
        self.bill_text = 'Сумма к оплате:\n'
        self.bill_count = 0
        self.bill.setText('')
        self.check.setText('')

    def new_order(self):
        self.order_id += 1
        self.bill.setText('')
        self.check.setText('')

    # функция показа блюд
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
            self.position_3_pick.setText('Картофель по деревенски')
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
            self.position_1_pick.setText('Кока-Кола')
            self.position_2_pick.setText('Спрайт')
            self.position_3_pick.setText('Меринда')
            self.position_4_pick.setText('Каппучино')
            self.position_5_pick.setText('Молочный коктейль')
            self.position_1_price.setText('70р')
            self.position_2_price.setText('70р')
            self.position_3_price.setText('70р')
            self.position_4_price.setText('90р')
            self.position_5_price.setText('100р')
        elif self.rest == 'Burger King' and self.category == 'Закуска':
            self.position_1_pick.setText('Луковые кольца')
            self.position_2_pick.setText('Сырные медальоны')
            self.position_3_pick.setText('Сырные медальоны с халапеньо')
            self.position_4_pick.setText('Чикен Фри')
            self.position_5_pick.setText('King GO')
            self.position_1_price.setText('60р')
            self.position_2_price.setText('90р')
            self.position_3_price.setText('100р')
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
            self.position_1_pick.setText('Вишнёвый сок')
            self.position_2_pick.setText('Липтон')
            self.position_3_pick.setText('ШефЛимонад')
            self.position_4_pick.setText('Чай')
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
            self.position_4_pick.setText('Куриная ножка')
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
