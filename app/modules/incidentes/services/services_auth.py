# app/modules/incidentes/services/services_auth.py
from sqlalchemy.orm import Session
from app.modules.incidentes.repositories import repositories_auth as repo

def authenticate_user(db: Session, username: str, password: str):
    user = repo.get_by_username(db, username)
    if not user:
        return None
    if getattr(user, "password", None) != password:
        return None
    return user

def get_user_roles(db: Session, id_usuario: int):
    return repo.get_roles_for_user(db, id_usuario)
