import random
import string
import datetime
from random import choice

from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from ..settings import engine, LENGTH_GENERATE


class BD:

    def write_one(self, model):
        with Session(engine) as session:
            try:
                session.add(model)
                session.commit()
            except IntegrityError:
                session.rollback()

    def write(self, data: list):
        with Session(engine) as session:
            for element in data:
                try:
                    session.add(element)
                    session.commit()
                except IntegrityError:
                    session.rollback()
                    continue

    def write_all(self, data: list):
        with Session(engine) as session:
            try:
                session.add_all(data)
            except IntegrityError:
                session.rollback()
                print("уже есть")
            session.commit()

    def get_one(self, model, filter_text):
        with Session(engine) as session:
            result = session.query(model).filter(text(filter_text)).first()
            return result


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


def generate_user(length=LENGTH_GENERATE):
    data = {
        "login": generate_random_string(length),
        "password": generate_random_string(length),
        "firstname": generate_random_string(length)
    }

    return data


def generate_order(length=LENGTH_GENERATE):
    def generate_metroStation():
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

    def generate_phone():
        phone = "+7"
        for _ in range(10):
            digit = choice(string.digits)
            phone += digit
        return phone

    def generate_renttime():
        while True:
            digit = int(choice(string.digits))
            if digit != 0:
                return digit

    def generate_date():
        date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        return date

    data = {
        "firstname": generate_random_string(length),
        "lastname": generate_random_string(length),
        "address": generate_random_string(length),
        "metroStation": generate_metroStation(),
        "phone": generate_phone(),
        "rentTime": generate_renttime(),
        "deliveryDate": generate_date(),
        "comment": generate_random_string(length),
    }

    return data
