from ..settings import engine

from .models import Base


def create_db_and_tables():
    Base.metadata.create_all(engine)
