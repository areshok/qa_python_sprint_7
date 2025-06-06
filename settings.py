import os
from pathlib import Path

from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent
USERS_FILE = os.path.join(BASE_DIR, "data/created_users.csv")
CHECK_USER_FILE = os.path.exists(USERS_FILE)

LENGTH_GENERATE = 10

CREATED_COURIER = {
    "login": "arstest",
    "password": "Arstest1",
    }


BD_FILE = os.path.join(BASE_DIR, "data/database.db")
DB = f"sqlite:///{BD_FILE}"
engine = create_engine(DB)
