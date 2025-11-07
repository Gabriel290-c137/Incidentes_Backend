# Incidentes / Bienestar Estudiantil - dto
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class IncidenteCreate(BaseModel):
    fecha: datetime
    lugar: Optional[str] = None
    descripcion: Optional[str] = None

    antecedentes: Optional[str] = None
    acciones_tomadas: Optional[str] = None
    seguimiento: Optional[str] = None
    estado: Optional[str] = "provisional"

    id_estudiantes: List[int] = []
    id_situaciones: List[int] = []

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
    fecha: datetime
    antecedentes: Optional[str] = None
    acciones_tomadas: Optional[str] = None
    seguimiento: Optional[str] = None
    estado: str
    estudiantes: List[EstudianteRead] = []
    adjuntos: List[AdjuntoRead] = []

    class Config:
        orm_mode = True
