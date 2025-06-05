import random
import string
import datetime
import csv
from random import choice

from ..settings import LENGTH_GENERATE, USERS_FILE, CHECK_USER_FILE


class Base:

    def __init_subclass__(cls, **kwargs):
        """Автоматически создает геттеры для всех атрибутов при создании подкласса"""
        super().__init_subclass__(**kwargs)

        init = cls.__dict__.get('__init__')
        if not init:
            return

        import inspect
        sig = inspect.signature(init)
        params = list(sig.parameters.keys())[1:]

        for param in params:
            if not hasattr(cls, param):
                def create_getter(name):
                    return property(lambda self, name=name: getattr(self, '_' + name))
                setattr(cls, '_' + param, None)
                setattr(cls, param, create_getter(param))


class Order(Base):
    def __init__(
            self
            ):
        super().__init__()
        self.firstname = self.generate_random_string(LENGTH_GENERATE)
        self.lastname = self.generate_random_string(LENGTH_GENERATE)
        self.address = self.generate_random_string(LENGTH_GENERATE)
        self.metroStation = self.generate_metroStation()
        self.phone = self.generate_phone()
        self.rentTime = self.generate_renttime()
        self.deliveryDate = self.generate_date()
        self.comment = self.generate_random_string(LENGTH_GENERATE)
        self.color = self.generate_color()

    def generate_random_string(self, length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    def generate_metroStation(self):
        metro_stations = [
            "Сокольники",
            "Красносельская",
            "Комсомольская",
            "Проспект Мира",
            "Новослободская",
            "Тверская",
            "Библиотека им. Ленина",
            "Парк культуры",
            "Фрунзенская",
            "Спортивная",
            "Киевская",
            "Кутузовская",
            "Студенческая",
            "Краснопресненская",
            "Алма-Атинская",
            "Дубровка",
            "Кожуховская",
            "Печатники",
            "Волжская",
            "Люблино"
        ]
        return choice(metro_stations)

    def generate_phone(self):
        phone = "+7"
        for _ in range(10):
            digit = choice(string.digits)
            phone += digit
        return phone

    def generate_renttime(self):
        while True:
            digit = int(choice(string.digits))
            if digit != 0:
                return digit

    def generate_date(self):
        date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        return date

    def generate_color(self):
        color = ["BLACK", "GRAY"]
        return [choice(color)]

    def get(self):
        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "address": self.address,
            "metroStation": self.metroStation,
            "phone": self.phone,
            "rentTime": self.rentTime,
            "deliveryDate": self.deliveryDate,
            "comment": self.comment,
            "color": self.color
        }

    def __str__(self):
        return str({
            "firstname": self.firstname,
            "lastname": self.lastname,
            "address": self.address,
            "metroStation": self.metroStation,
            "phone": self.phone,
            "rentTime": self.rentTime,
            "deliveryDate": self.deliveryDate,
            "comment": self.comment,
            "color": self.color
        })


class User(Base):
    def __init__(self):
        self.login = self.__generate_random_string(LENGTH_GENERATE)
        self.password = self.__generate_random_string(LENGTH_GENERATE)
        self.firstname = self.__generate_random_string(LENGTH_GENERATE)

    def __generate_random_string(self, length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    def get(self):
        return {
            "login": self.login,
            "password": self.password,
            "firstname": self.firstname
        }

    def create(self, length=LENGTH_GENERATE):
        self.login = self.__generate_random_string(length)
        self.password = self.__generate_random_string(length)
        self.firstname = self.__generate_random_string(length)

    def save(self):
        data = self.get()
        if data['login'] is not None:
            with open(USERS_FILE, mode="+a", encoding="utf-8") as file:
                filed_names = ["login", "password", "firstname"]
                write = csv.DictWriter(file, fieldnames=filed_names, delimiter=";")
                if not CHECK_USER_FILE:
                    write.writeheader()
                write.writerow(data)

    def __str__(self):
        return str({
            "login": self.login,
            "password": self.password,
            "firstname": self.firstname
        })
