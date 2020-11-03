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

    def edit_order(self, item):
        pass

    def delete_order(self, item):
        pass


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
        self.name = str(values[1])

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_list(self, with_id=False):
        if with_id:
            return [self.id, self.name]
        else:
            return [self.name]
