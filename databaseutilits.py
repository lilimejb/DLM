import sqlite3


# класс для удобства работы с БД
class Database:
    def __init__(self, name):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()

    def get_total_result(self, table):
        pass

    def add_person(self, person):
        self.cursor.execute(f"""INSERT INTO Persons (name, surname)
                VALUES(?, ?)""", person.get_list())
        self.connection.commit()

    def add_order(self, order):
        self.cursor.execute(f"""INSERT INTO Orders (id, restaurant_id, person_id)
                VALUES(?, ?, ?)""", order.get_list(True))
        self.connection.commit()
        return order.get_id()

    def add_relation(self, relation):
        self.cursor.execute(f"""INSERT INTO Relations (order_id, dish_id, amount)
                        VALUES(?, ?, ?)""", relation.get_list())
        self.connection.commit()

    def get_relation(self, order_id):
        values = self.cursor.execute(f'''SELECT dish_id, amount FROM Relations 
                                        WHERE order_id = "{order_id}"''').fetchall()
        return values

    def get_order(self, person_id, with_id=False):
        values = self.cursor.execute(f'''SELECT * FROM Orders WHERE person_id = "{person_id}"''').fetchall()
        it = Order(*values)
        return it.get_list(with_id)

    def get_dish(self, item, with_id=False):
        values = self.cursor.execute(f'''SELECT * FROM Dishes WHERE name = "{item}"''').fetchall()
        it = Dish(*values)
        return it.get_list(with_id)

    def get_dish_name(self, dish_id):
        values = self.cursor.execute(f'''SELECT * FROM Dishes WHERE id = "{dish_id}"''').fetchall()
        it = Dish(*values)
        return it.get_name()

    def get_person(self, name, surname, with_id=False):
        values = self.cursor.execute(f'''SELECT * FROM Persons
                                        WHERE name = "{name}" and surname = "{surname}"''').fetchall()
        it = Person(*values)
        return it.get_list(with_id)

    def get_restaurant_id(self, name):
        values = self.cursor.execute(f'''SELECT * FROM Restaurants WHERE name = "{name}"''').fetchall()
        it = Restaurant(*values)
        return it.get_id()

    def get_restaurant_name(self, rest_id):
        values = self.cursor.execute(f'''SELECT * FROM Restaurants WHERE id = "{rest_id}"''').fetchall()
        it = Restaurant(*values)
        return it.get_name()


# класс для удобства работы с блюдами
class Dish:
    def __init__(self, values):
        self.id = values[0]
        self.name = str(values[1])
        self.category = values[2]
        self.price = values[3]

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_category(self):
        return self.category

    def get_price(self):
        return self.price

    def get_list(self, with_id=False):
        if with_id:
            return [self.id, self.name, self.category, self.price]
        else:
            return [self.name, self.category, self.price]


# класс для удобства работы с людьми
class Person:
    def __init__(self, values):
        self.id = values[0]
        self.name = str(values[1])
        self.surname = str(values[2])

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_surname(self):
        return self.surname

    def get_list(self, with_id=False):
        if with_id:
            return [self.id, self.name, self.surname]
        else:
            return [self.name, self.surname]


# класс для удобства работы с ресторанами
class Restaurant:
    def __init__(self, values):
        self.id = values[0]
        self.name = values[1]

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_list(self, with_id=False):
        if with_id:
            return [self.id, self.name]
        else:
            return [self.name]


# класс для удобства работы с заказами
class Order:
    def __init__(self, values):
        self.id = values[0]
        self.restaurant_id = values[1]
        self.person_id = values[2]

    def get_id(self):
        return self.id

    def get_restaurant_id(self):
        return self.restaurant_id

    def get_person_id(self):
        return self.person_id

    def get_list(self, with_id=False):
        if with_id:
            return [self.id, self.restaurant_id, self.person_id]
        else:
            return [self.restaurant_id, self.person_id]


# класс для удобства работы с "связками"
class Relation:
    def __init__(self, values):
        self.order_id = values[0]
        self.person_id = values[1]
        self.amount = values[2]

    def get_order_id(self):
        return self.order_id

    def get_person_id(self):
        return self.person_id

    def get_amount(self):
        return self.amount

    def get_list(self):
        return [self.order_id, self.person_id, self.amount]
