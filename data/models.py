
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer, ForeignKey


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)
    firstname = Column(String)


class Color(Base):
    __tablename__ = "color"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class Station(Base):
    __tablename__ = "station"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    address = Column(String)
    metroStation = Column(Integer, ForeignKey("station.id"))
    phone = Column(String(12))
    rentTime = Column(Integer)
    deliveryDate = Column(String)
    comment = Column(String)
    color = Column(Integer, ForeignKey("color.id"))
