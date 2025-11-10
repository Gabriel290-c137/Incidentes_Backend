# app/modules/incidentes/dto/dto_auth.py
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional


class UsuarioCreate(BaseModel):
    usuario: str = Field(..., min_length=3)
    correo: EmailStr
    password: str = Field(..., min_length=6)
    id_persona: int = 0
    rol: Optional[str] = "regente"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    roles: Optional[List[str]] = []
