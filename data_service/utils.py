import requests
import json
import config
from sqlalchemy.orm import Session

from database import engine


def get_db():
    with Session(engine) as session:
        yield session
