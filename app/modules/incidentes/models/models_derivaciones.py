# app/modules/incidentes/models/models_derivaciones.py
from sqlalchemy import Column, Integer, DateTime, Text, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base

# Modelo para tabla estado (si ya existe en otro módulo puedes importarlo en su lugar)
class Estado(Base):
    __tablename__ = "estado"
    id_estado = Column(Integer, primary_key=True, index=True)
    nombre_estado = Column(String(50), nullable=False)
    descripcion = Column(String(255), nullable=True)


class Derivacion(Base):
    __tablename__ = "derivaciones"
    id_derivacion = Column(Integer, primary_key=True, index=True)
    id_incidente = Column(Integer, ForeignKey("incidentes.id_incidente"), nullable=False)
    id_quien_deriva = Column(Integer, ForeignKey("personas.id_persona"), nullable=False)
    id_quien_recibe = Column(Integer, ForeignKey("personas.id_persona"), nullable=False)
    fecha_derivacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    id_estado_antes = Column(Integer, ForeignKey("estado.id_estado"), nullable=True)
    id_estado_despues = Column(Integer, ForeignKey("estado.id_estado"), nullable=True)
    observaciones = Column(Text, nullable=True)

    # Relaciones ORM para consultas cómodas
    incidente = relationship("Incidente", backref="derivaciones")
    quien_deriva = relationship("Persona", foreign_keys=[id_quien_deriva], viewonly=True)
    quien_recibe = relationship("Persona", foreign_keys=[id_quien_recibe], viewonly=True)
    estado_antes = relationship("Estado", foreign_keys=[id_estado_antes], viewonly=True)
    estado_despues = relationship("Estado", foreign_keys=[id_estado_despues], viewonly=True)
