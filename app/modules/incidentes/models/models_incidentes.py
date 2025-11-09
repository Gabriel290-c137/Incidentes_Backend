# Incidentes / Bienestar Estudiantil - models
from sqlalchemy import Column, Integer, DateTime, Text, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base

# Many-to-many tables
incidentes_estudiantes = Table(
    "incidentes_estudiantes",
    Base.metadata,
    Column("id_incidente", Integer, ForeignKey("incidentes.id_incidente"), primary_key=True),
    Column("id_estudiante", Integer, ForeignKey("estudiantes.id_estudiante"), primary_key=True),
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
    titulo = Column(String(100), nullable=False)                # <-- NUEVO
    fecha = Column(DateTime, nullable=False, default=datetime.utcnow)
    antecedentes = Column(Text, nullable=True)
    acciones_tomadas = Column(Text, nullable=True)
    seguimiento = Column(Text, nullable=True)
    estado = Column(String(20), nullable=False, default="provisional")
    creado_por = Column(Integer, ForeignKey("personas.id_persona"), nullable=True)  # <-- NUEVO

    estudiantes = relationship("Estudiante", secondary=incidentes_estudiantes, back_populates="incidentes")
    situaciones = relationship("SituacionIncidente", secondary=incidentes_situaciones, back_populates="incidentes")
    adjuntos = relationship("Adjunto", back_populates="incidente", cascade="all, delete-orphan")


class Estudiante(Base):
    __tablename__ = "estudiantes"
    id_estudiante = Column(Integer, primary_key=True, index=True)
    nombres = Column(String(50), nullable=False)
    apellido_paterno = Column(String(50), nullable=False)
    apellido_materno = Column(String(50), nullable=False)

    incidentes = relationship("Incidente", secondary=incidentes_estudiantes, back_populates="estudiantes")


class SituacionIncidente(Base):
    __tablename__ = "situaciones_incidente"
    id_situacion = Column(Integer, primary_key=True)
    id_area = Column(Integer)
    nombre_situacion = Column(String(50))
    nivel_gravedad = Column(String(20))

    incidentes = relationship("Incidente", secondary=incidentes_situaciones, back_populates="situaciones")


# Modelo para adjuntos (opcional en tu DDL original, lo agregamos para persistir archivos)
class Adjunto(Base):
    __tablename__ = "adjuntos"
    id_adjunto = Column(Integer, primary_key=True, index=True)
    id_incidente = Column(Integer, ForeignKey("incidentes.id_incidente"), nullable=False)
    nombre_archivo = Column(String(255), nullable=False)
    ruta = Column(String(1024), nullable=False)
    tipo_mime = Column(String(100), nullable=True)
    subido_por = Column(Integer, nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow)

    incidente = relationship("Incidente", back_populates="adjuntos")
