# Configuración de la base de datos
# from app.core.extensions import db

# def init_database(app):
#     """
#     Inicializar base de datos con datos de prueba
#     """
#     with app.app_context():
#         # Crear todas las tablas
#         db.create_all()
        
#         print("✅ Base de datos inicializada correctamente")

# def reset_database(app):
#     """
#     Resetear la base de datos
#     """
#     with app.app_context():
#         db.drop_all()
#         db.create_all()
        
#         print("🔄 Base de datos reseteada correctamente")

# app/config/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:@127.0.0.1:3306/bienestar_estudiantil_")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
