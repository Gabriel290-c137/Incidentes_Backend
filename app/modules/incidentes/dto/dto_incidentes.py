# app/modules/incidentes/dto/dto_incidentes.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class IncidenteCreate(BaseModel):
    antecedentes: Optional[str] = None
    acciones_tomadas: Optional[str] = None
    seguimiento: Optional[str] = None

    id_estudiantes: List[int] = Field(..., min_items=1)
    id_situaciones: List[int] = Field(..., min_items=1)

    # campo opcional para pruebas: id_persona creador
    creado_por: Optional[int] = None

    class Config:
        orm_mode = True


class EstudianteRead(BaseModel):
    id_estudiante: int
    ci: Optional[str] = None
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
    fecha_subida: datetime

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
    # ya no existe creado_por en la tabla; si quieres devolver quien creó, puedes leer historial.
    class Config:
        orm_mode = True

class IncidenteUpdate(BaseModel):
    antecedentes: Optional[str] = None
    acciones_tomadas: Optional[str] = None
    seguimiento: Optional[str] = None
    id_estudiantes: Optional[List[int]] = None
    id_situaciones: Optional[List[int]] = None
    estado: Optional[str] = None  # ← NUEVO

    class Config:
        orm_mode = True
