# app/modules/incidentes/controllers/controllers_auth.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_session
from app.modules.incidentes.repositories import repositories_auth as repo

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/whoami")
def whoami(db: Session = Depends(get_session)):
    persona = repo.get_persona_by_id(db, 1)
    roles = repo.get_roles_for_persona(db, persona.id_persona) if persona else []
    return {"persona": persona, "roles": roles}
