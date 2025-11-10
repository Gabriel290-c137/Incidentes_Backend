# app/modules/incidentes/models/models_incidentes.py
from sqlalchemy import Column, Integer, DateTime, Text, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base

incidentes_estudiantes = Table(
    "incidentes_estudiantes",
    Base.metadata,
    Column("id_incidente", Integer, ForeignKey("incidentes.id_incidente"), primary_key=True),
    Column("id_estudiante", Integer, ForeignKey("estudiantes.id_estudiante"), primary_key=True),
)

incidentes_profesores = Table(
    "incidentes_profesores",
    Base.metadata,
    Column("id_incidente", Integer, ForeignKey("incidentes.id_incidente"), primary_key=True),
    Column("id_profesor", Integer, ForeignKey("personas.id_persona"), primary_key=True),
)

incidentes_situaciones = Table(
    "incidentes_situaciones",
    Base.metadata,
    Column("id_incidente", Integer, ForeignKey("incidentes.id_incidente"), primary_key=True),
    Column("id_situacion", Integer, ForeignKey("situaciones_incidente.id_situacion"), primary_key=True),
)

class Incidente(Base):
    __tablename__ = "incidentes"
    id_incidente = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, nullable=False, default=datetime.utcnow)
    antecedentes = Column(Text, nullable=True)
    acciones_tomadas = Column(Text, nullable=True)
    seguimiento = Column(Text, nullable=True)
    estado = Column(String(20), nullable=False, default="provisional")
    # quitamos creado_por (ya no está en la tabla)

    estudiantes = relationship("Estudiante", secondary=incidentes_estudiantes, back_populates="incidentes")
    situaciones = relationship("SituacionIncidente", secondary=incidentes_situaciones, back_populates="incidentes")
    adjuntos = relationship("Adjunto", back_populates="incidente", cascade="all, delete-orphan")


class Estudiante(Base):
    __tablename__ = "estudiantes"
    id_estudiante = Column(Integer, primary_key=True, index=True)
    ci = Column(String(20))
    nombres = Column(String(50), nullable=False)
    apellido_paterno = Column(String(50), nullable=False)
    apellido_materno = Column(String(50), nullable=False)
    fecha_nacimiento = Column(DateTime)
    direccion = Column(String(100))
    nombre_padre = Column(String(50))
    apellido_paterno_padre = Column(String(50))
    apellido_materno_padre = Column(String(50))
    telefono_padre = Column(String(20))
    nombre_madre = Column(String(50))
    apellido_paterno_madre = Column(String(50))
    apellido_materno_madre = Column(String(50))
    telefono_madre = Column(String(20))

    incidentes = relationship("Incidente", secondary=incidentes_estudiantes, back_populates="estudiantes")


class SituacionIncidente(Base):
    __tablename__ = "situaciones_incidente"
    id_situacion = Column(Integer, primary_key=True)
    id_area = Column(Integer)
    nombre_situacion = Column(String(50))
    nivel_gravedad = Column(String(20))

    incidentes = relationship("Incidente", secondary=incidentes_situaciones, back_populates="situaciones")


class Adjunto(Base):
    __tablename__ = "adjuntos"
    id_adjunto = Column(Integer, primary_key=True, index=True)
    id_incidente = Column(Integer, ForeignKey("incidentes.id_incidente"), nullable=False)
    nombre_archivo = Column(String(255), nullable=False)
    ruta = Column(String(1024), nullable=False)
    tipo_mime = Column(String(100), nullable=True)
    subido_por = Column(Integer, nullable=True)
    fecha_subida = Column(DateTime, default=datetime.utcnow)

    incidente = relationship("Incidente", back_populates="adjuntos")


# Nuevo modelo: historial_de_modificaciones
from sqlalchemy import Text as SQLText

class HistorialDeModificacion(Base):
    __tablename__ = "historial_de_modificaciones"
    id_historial = Column(Integer, primary_key=True, index=True)
    id_incidente = Column(Integer, ForeignKey("incidentes.id_incidente"), nullable=False)
    id_persona = Column(Integer, ForeignKey("personas.id_persona"), nullable=True)
    fecha_cambio = Column(DateTime, default=datetime.utcnow)
    campo_modificado = Column(String(100))
    valor_anterior = Column(SQLText, nullable=True)
    valor_nuevo = Column(SQLText, nullable=True)
