from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Importar los modelos para registrarlos en Base.metadata
from . import models


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Crea todas las tablas definidas en los modelos"""
    try:
        Base.metadata.create_all(bind=engine)
        print(" Tablas creadas/verificadas en la base de datos")
    except Exception as e:
        print(f" Error al crear las tablas: {e}")


def test_connection():
    try:
        with engine.connect() as conn:
            print(" Conexión a la base de datos exitosa.")
    except Exception as e:
        print(f" Error al conectar a la base de datos: {e}")
