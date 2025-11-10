# app/modules/incidentes/dto/dto_modificaciones.py
from pydantic import BaseModel, Field
from typing import List, Optional

class ModificacionUpdate(BaseModel):
    antecedentes: Optional[str] = None
    acciones_tomadas: Optional[str] = None
    seguimiento: Optional[str] = None
    estado: Optional[str] = None  # ejemplo: "provisional","derivado","cerrado"
    id_estudiantes: Optional[List[int]] = None
    id_situaciones: Optional[List[int]] = None

    # quien realiza la modificación (opcional, si tu auth lo provee omitir aquí)
    id_persona: Optional[int] = None

    class Config:
        orm_mode = True
