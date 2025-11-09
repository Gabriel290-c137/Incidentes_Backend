# app/modules/incidentes/dto/incidentes_dto.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class IncidenteCreate(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=100)   # obligatorio
    lugar: Optional[str] = None
    descripcion: Optional[str] = None

    antecedentes: Optional[str] = None
    acciones_tomadas: Optional[str] = None
    seguimiento: Optional[str] = None
    # NO pedir fecha: se genera en el servidor
    id_estudiantes: List[int] = Field(..., min_items=1)      # obligatorio
    id_situaciones: List[int] = Field(..., min_items=1)      # obligatorio

    class Config:
        orm_mode = True

class EstudianteRead(BaseModel):
    id_estudiante: int
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    class Config:
        orm_mode = True

class AdjuntoRead(BaseModel):
    id_adjunto: int
    nombre_archivo: str
    ruta: str
    tipo_mime: Optional[str] = None
    subido_por: Optional[int] = None
    creado_en: datetime
    class Config:
        orm_mode = True

class IncidenteRead(BaseModel):
    id_incidente: int
    titulo: str
    fecha: datetime
    antecedentes: Optional[str] = None
    acciones_tomadas: Optional[str] = None
    seguimiento: Optional[str] = None
    estado: str
    estudiantes: List[EstudianteRead] = []
    adjuntos: List[AdjuntoRead] = []
    creado_por: Optional[int] = None
    class Config:
        orm_mode = True