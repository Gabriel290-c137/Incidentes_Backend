# Incidentes / Bienestar Estudiantil - controllers
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import os, shutil
from app.config.database import get_session
from app.modules.incidentes.dto import IncidenteCreate, IncidenteRead
from app.modules.incidentes.services.incidentes_service import IncidenteService

router = APIRouter(prefix="/incidentes", tags=["incidentes"])

MEDIA_DIR = os.getenv("MEDIA_DIR", "uploads")
os.makedirs(MEDIA_DIR, exist_ok=True)


@router.post("/", response_model=IncidenteRead)
def create_incidente_endpoint(incidente: IncidenteCreate, db: Session = Depends(get_session)):
    svc = IncidenteService(db)
    created = svc.create_incidente(incidente)
    return created


@router.post("/{id_incidente}/adjuntos/")
def upload_adjunto(id_incidente: int, file: UploadFile = File(...), subido_por: int | None = None, db: Session = Depends(get_session)):
    svc = IncidenteService(db)

    # verifica existencia del incidente
    inc = svc.db.query(svc.repo.db.bind.mapper_registry._class_registry.get("Incidente")).filter_by(id_incidente=id_incidente).first()
    # Nota: la línea anterior es un fallback raro si no quieres importar models aquí;
    # para mayor claridad reemplázala por:
    # from app.modules.incidentes.models import Incidente
    # inc = db.query(Incidente).filter(Incidente.id_incidente == id_incidente).first()
    # (prefiero la segunda; la dejo comentada arriba)

    # Mejor: usa el repositorio para obtener el incidente:
    inc = svc.repo.get(id_incidente)
    if not inc:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")

    filename = file.filename
    dest_path = os.path.join(MEDIA_DIR, f"{id_incidente}_{filename}")
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        adj = svc.upload_adjunto(id_incidente, filename, dest_path, file.content_type, subido_por)
        return {"ok": True, "adjunto_id": getattr(adj, "id_adjunto", None)}
    except ValueError:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
