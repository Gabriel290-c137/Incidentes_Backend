# app/modules/incidentes/dto/dto_derivaciones.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class DerivacionCreate(BaseModel):
    id_incidente: int
    id_quien_deriva: int
    id_quien_recibe: int
    id_estado_despues: Optional[int] = None
    observaciones: Optional[str] = None

    class Config:
        orm_mode = True


class PersonaSimple(BaseModel):
    id_persona: int
    ci: Optional[str] = None
    nombres: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None

    class Config:
        orm_mode = True


class EstadoRead(BaseModel):
    id_estado: int
    nombre_estado: str
    descripcion: Optional[str] = None

    class Config:
        orm_mode = True


class DerivacionRead(BaseModel):
    id_derivacion: int
    id_incidente: int
    id_quien_deriva: int
    id_quien_recibe: int
    fecha_derivacion: datetime
    id_estado_antes: Optional[int] = None
    id_estado_despues: Optional[int] = None
    observaciones: Optional[str] = None

    quien_deriva: Optional[PersonaSimple] = None
    quien_recibe: Optional[PersonaSimple] = None
    estado_antes: Optional[EstadoRead] = None
    estado_despues: Optional[EstadoRead] = None

    class Config:
        orm_mode = True
