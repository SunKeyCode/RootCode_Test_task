import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

if os.environ.get("DEBUG") == "true":
    DEBUG = True
else:
    DEBUG = False

DB_NAME = os.environ.get("DB_NAME")
DB_NAME_TEST = os.environ.get("DB_NAME_TEST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")

DB_URL = "postgresql+asyncpg://{user}:{password}@{host}/{db_name}".format(
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    db_name=DB_NAME,
)

# main.py directory
BASE_DIR = Path(__file__).resolve().parents[1]

FILES_DIR = BASE_DIR.parents[1] / "files"
