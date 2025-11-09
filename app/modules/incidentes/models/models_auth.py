# app/modules/incidentes/models/models_auth.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base

class Persona(Base):
    __tablename__ = "personas"
    id_persona = Column(Integer, primary_key=True, index=True)
    ci = Column(String(20), nullable=False)
    nombres = Column(String(50), nullable=False)
    apellido_paterno = Column(String(50), nullable=False)
    apellido_materno = Column(String(50), nullable=False)
    direccion = Column(String(100))
    telefono = Column(String(20))
    correo = Column(String(50))
    tipo_persona = Column(String(50))

class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, index=True)
    id_persona = Column(Integer, ForeignKey("personas.id_persona"), nullable=False)
    usuario = Column(String(50), unique=True, nullable=False)
    correo = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    persona = relationship("Persona", backref="usuario", foreign_keys=[id_persona])

class UsuarioRol(Base):
    __tablename__ = "usuario_roles"
    # Simplificamos el mapeo: usamos columnas normales; la PK compuesta la maneja la DB
    id_usuario = Column(Integer, primary_key=True)
    id_rol = Column(Integer, primary_key=True)
    fecha_inicio = Column(DateTime, primary_key=True, default=datetime.utcnow)
    fecha_fin = Column(DateTime, nullable=True)
    estado = Column(String(20), nullable=False)

class Rol(Base):
    __tablename__ = "roles"
    id_rol = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    descripcion = Column(String(255))

class LoginLog(Base):
    __tablename__ = "login_logs"
    id_log = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    fecha_hora = Column(DateTime, default=datetime.utcnow)
