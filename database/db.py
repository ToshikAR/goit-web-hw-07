import configparser
import pathlib
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

user = os.getenv("DBM07_USER")
password = os.getenv("DBM07_PASSWORD")
domain = os.getenv("DBM07_HOST")
port = os.getenv("DBM07_PORT")
db = os.getenv("DBM07_DB")

# URI: postgresql://username:password@domain:port/database
URL = f"postgresql://{user}:{password}@{domain}:{port}/{db}"
print(URL)

engine = create_engine(URL, echo=True, pool_size=5, max_overflow=0)
DBSession = sessionmaker(bind=engine)
session = DBSession()
