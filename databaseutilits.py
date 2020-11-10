import sqlite3


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
        self.cursor.execute(f"""INSERT INTO Orders (restaurant_id, person_id)
                VALUES(?, ?)""", order.get_list())
        self.connection.commit()

    def edit_order(self, item):
        pass

    def delete_order(self, item):
        pass

    def add_relation(self, relation):
        self.cursor.execute(f"""INSERT INTO Relations (order_id, dish_id, amount)
                        VALUES(?, ?, ?)""", relation.get_list())
        self.connection.commit()

    def get_order(self, person_id, with_id=False):
        values = self.cursor.execute(f'''SELECT * FROM Orders WHERE person_id = "{person_id}"''').fetchall()
        it = Order(*values)
        return it.get_list(with_id)

    def get_dish(self, item, with_id=False):
        values = self.cursor.execute(f'''SELECT * FROM Dishes WHERE name = "{item}"''').fetchall()
        it = Dish(*values)
        return it.get_list(with_id)

    def get_person(self, name, with_id=False):
        values = self.cursor.execute(f'''SELECT * FROM Persons WHERE name = "{name}"''').fetchall()
        it = Person(*values)
        return it.get_list(with_id)

    def get_restaurant(self, name, with_id=False):
        values = self.cursor.execute(f'''SELECT * FROM Restaurants WHERE name = "{name}"''').fetchall()
        it = Restaurant(*values)
        return it.get_list(with_id)


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
