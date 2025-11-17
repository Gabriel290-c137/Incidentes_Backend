# app/modules/incidentes/controllers/controllers_incidentes.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
import os, shutil
from typing import Optional, List

from app.config.database import get_session
from app.modules.incidentes.dto.dto_incidentes import IncidenteCreate, IncidenteRead
from app.modules.incidentes.services.services_incidentes import IncidenteService
from app.modules.incidentes.dto.dto_incidentes import IncidenteUpdate

router = APIRouter(prefix="/incidentes", tags=["incidentes"])

MEDIA_DIR = os.getenv("MEDIA_DIR", "uploads")
os.makedirs(MEDIA_DIR, exist_ok=True)


@router.post("/", response_model=IncidenteRead, status_code=status.HTTP_201_CREATED)
def create_incidente_endpoint(incidente: IncidenteCreate, db: Session = Depends(get_session)):

    svc = IncidenteService(db)

    creador_id = incidente.creado_por # or 1   por defecto persona id=1

    try:
        creado = svc.create_incidente(incidente, creador_persona_id=creador_id)
        return creado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # imprime traza en consola para debugging si lo necesitas (opcional)
        raise HTTPException(status_code=500, detail="Error interno")
    
    
@router.get("/", response_model=List[IncidenteRead])
def get_all_incidentes(db: Session = Depends(get_session)):
    svc = IncidenteService(db)
    incidentes = svc.get_all_incidentes()
    return incidentes


@router.post("/{id_incidente}/adjuntos/")
def upload_adjunto(id_incidente: int, file: UploadFile = File(...), db: Session = Depends(get_session), subido_por: int | None = None):
    svc = IncidenteService(db)
    inc = svc.repo.get(id_incidente)
    if not inc:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
    filename = file.filename
    dest_path = os.path.join(MEDIA_DIR, f"{id_incidente}_{filename}")
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    adj = svc.upload_adjunto(id_incidente, filename, dest_path, file.content_type, subido_por=subido_por)
    return {"ok": True, "adjunto_id": getattr(adj, "id_adjunto", None)}


@router.get("/{id_incidente}", response_model=IncidenteRead)
def get_incidente_by_id(id_incidente: int, db: Session = Depends(get_session)):
    svc = IncidenteService(db)
    incidente = svc.repo.get(id_incidente)
    if not incidente:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
    return incidente


@router.put("/{id_incidente}", response_model=IncidenteRead)
def update_incidente_endpoint(
    id_incidente: int,
    update_data: IncidenteUpdate,
    db: Session = Depends(get_session),
    modificador_id: Optional[int] = None  # puedes pasarlo en headers o auth
):
    svc = IncidenteService(db)
    try:
        actualizado = svc.update_incidente(
            id_incidente=id_incidente,
            update_data=update_data,
            modificador_persona_id=modificador_id or 1  # fallback
        )
        return actualizado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno al actualizar")
