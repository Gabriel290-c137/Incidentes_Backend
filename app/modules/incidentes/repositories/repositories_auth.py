# app/modules/incidentes/repositories/repositories_auth.py
from sqlalchemy.orm import Session
from datetime import datetime
from app.modules.incidentes.models.models_auth import Usuario, UsuarioRol, Rol, LoginLog

def get_by_username(db: Session, username: str):
    return db.query(Usuario).filter(Usuario.usuario == username).first()

def get_roles_for_user(db: Session, id_usuario: int):
    rows = (
        db.query(Rol.nombre)
        .join(UsuarioRol, UsuarioRol.id_rol == Rol.id_rol)
        .filter(UsuarioRol.id_usuario == id_usuario)
        .filter(UsuarioRol.estado == 'activo')
        .all()
    )
    return [r[0] for r in rows] if rows else []

def log_login(db: Session, id_usuario: int):
    log = LoginLog(id_usuario=id_usuario, fecha_hora=datetime.utcnow())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
