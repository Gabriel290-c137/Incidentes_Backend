# app/modules/incidentes/controllers/controllers_derivaciones.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_session
from app.modules.incidentes.dto.dto_derivaciones import DerivacionCreate, DerivacionRead
from app.modules.incidentes.services.services_derivaciones import DerivacionService

router = APIRouter(prefix="/derivaciones", tags=["derivaciones"])


@router.post("/", response_model=DerivacionRead, status_code=status.HTTP_201_CREATED)
def create_derivacion_endpoint(payload: DerivacionCreate, db: Session = Depends(get_session)):
    svc = DerivacionService(db)
    try:
        creado = svc.create_derivacion(payload)
        return creado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al crear derivación")


@router.get("/incidente/{id_incidente}", response_model=list[DerivacionRead])
def list_derivaciones_incidente(id_incidente: int, db: Session = Depends(get_session)):
    svc = DerivacionService(db)
    derivs = svc.list_by_incidente(id_incidente)
    return derivs


@router.get("/{id_derivacion}", response_model=DerivacionRead)
def get_derivacion(id_derivacion: int, db: Session = Depends(get_session)):
    svc = DerivacionService(db)
    d = svc.get_derivacion(id_derivacion)
    if not d:
        raise HTTPException(status_code=404, detail="Derivación no encontrada")
    return d
