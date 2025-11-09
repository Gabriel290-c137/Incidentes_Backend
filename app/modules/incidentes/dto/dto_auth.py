# app/modules/incidentes/dto/dto_auth.py
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class UsuarioCreate(BaseModel):
    usuario: str = Field(..., min_length=3)
    correo: EmailStr
    password: str = Field(..., min_length=6)
    id_persona: int
    rol: Optional[str] = "regente"

class LoginRequest(BaseModel):
    usuario: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    roles: Optional[List[str]] = []

class UsuarioRead(BaseModel):
    id_usuario: int
    usuario: str
    correo: str
    id_persona: int
    class Config:
        orm_mode = True
