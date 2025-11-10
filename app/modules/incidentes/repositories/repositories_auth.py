# app/modules/incidentes/repositories/repositories_auth.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.modules.incidentes.models.models_auth import Usuario, UsuarioRol, Rol, Persona

def get_by_username(db: Session, username: str):
    return db.query(Usuario).filter(Usuario.usuario == username).first()

def get_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.correo == email).first()

def get_by_id(db: Session, id_usuario: int):
    return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

def get_persona_by_id(db: Session, id_persona: int):
    return db.query(Persona).filter(Persona.id_persona == id_persona).first()

def get_roles_for_user(db: Session, id_usuario: int):
    rows = (
        db.query(Rol.nombre)
        .join(UsuarioRol, UsuarioRol.id_rol == Rol.id_rol)
        .filter(UsuarioRol.id_usuario == id_usuario)
        .filter(UsuarioRol.estado == 'activo')
        .all()
    )
    return [r[0] for r in rows] if rows else []

def get_roles_for_persona(db: Session, id_persona: int):
    """
    Busca roles para la persona obteniendo el usuario asociado (si lo hay).
    """
    user = db.query(Usuario).filter(Usuario.id_persona == id_persona).first()
    if not user:
        return []
    return get_roles_for_user(db, user.id_usuario)
