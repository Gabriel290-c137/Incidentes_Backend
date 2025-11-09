# app/modules/incidentes/services/services_auth.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from types import SimpleNamespace
from typing import Optional
from sqlalchemy.orm import Session
import os

from app.config.database import get_session
from app.modules.incidentes.repositories import repositories_auth as repo
from app.modules.incidentes.models.models_auth import Usuario

# Config - mueve a .env en producción
SECRET_KEY = os.getenv("SECRET_KEY", "CAMBIA_ ESTA_CLAVE_POR_OTRA_MUY_SEGURA")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 6

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(db: Session, username: str, password: str):
    user = repo.get_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    """
    Decodifica token y:
        - si existe usuario en BD lo devuelve (adjuntando roles),
        - si no existe (ej: token dev) crea un objecto ligero con usuario/id_persona/roles.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas o token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise credentials_exception

    username = payload.get("sub")
    if username is None:
        raise credentials_exception

    # Intentamos buscar usuario real
    user = repo.get_by_username(db, username)
    if user:
        # poblar roles desde BD
        user.roles = repo.get_roles_for_user(db, user.id_usuario)
        return user

    # No existe en BD -> asumimos token dev: extraemos id_persona y roles del payload
    id_persona = payload.get("id_persona")
    roles = payload.get("roles", [])
    # retornamos un objeto ligero con la misma interfaz usada por el resto del código
    return SimpleNamespace(usuario=username, id_persona=id_persona, roles=roles)

def get_user_roles(db: Session, id_usuario: int):
    return repo.get_roles_for_user(db, id_usuario)
