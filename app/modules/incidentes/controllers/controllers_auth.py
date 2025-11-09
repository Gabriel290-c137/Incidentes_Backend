# app/modules/incidentes/controllers/controllers_auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os

from app.config.database import get_session
from app.modules.incidentes.services import services_auth as svc
from app.modules.incidentes.repositories import repositories_auth as repo

router = APIRouter(prefix="/auth", tags=["auth"])

class DevTokenRequest(BaseModel):
    id_persona: int
    usuario: str = "dev_user"
    roles: list[str] = ["regente"]

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    """
    Login real: usa credenciales almacenadas en DB.
    Responde con access_token (Bearer).
    """
    user = svc.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    roles = svc.get_user_roles(db, user.id_usuario)
    token_data = {"sub": user.usuario, "id_persona": user.id_persona, "roles": roles}
    access_token = svc.create_access_token(token_data)
    try:
        repo.log_login(db, user.id_usuario)
    except Exception:
        pass
    return {"access_token": access_token, "token_type": "bearer", "roles": roles}

@router.post("/dev-token")
def dev_token(payload: DevTokenRequest):
    """
    Genera un token de desarrollo que contiene id_persona y roles.
    SOLO en entorno dev: controlar con ENV var ENV=dev
    """
    if os.getenv("ENV", "dev") != "dev":
        raise HTTPException(status_code=403, detail="Dev tokens deshabilitados")
    token_data = {"sub": payload.usuario, "id_persona": payload.id_persona, "roles": payload.roles}
    access_token = svc.create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/whoami")
def whoami(current_user = Depends(svc.get_current_user)):
    """
    Devuelve el usuario actual basado en token.
    current_user tiene atributos:
        - usuario
        - id_persona
        - roles
    """
    return {"usuario": current_user.usuario, "id_persona": getattr(current_user, "id_persona", None), "roles": getattr(current_user, "roles", [])}
