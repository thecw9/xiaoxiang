import os
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# POSTGRES_HOST = "192.168.4.132"
# POSTGRES_PORT = "55432"
# POSTGRES_DB = "csust"
# POSTGRES_USER = "his"
# POSTGRES_PASSWORD = "His%409700"

POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
POSTGRES_DB = "pcs9700"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "His%409700"
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
