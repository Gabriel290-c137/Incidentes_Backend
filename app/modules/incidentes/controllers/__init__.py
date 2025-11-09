# # app/modules/incidentes/controllers/controllers_incidentes.py
# from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
# from sqlalchemy.orm import Session
# import os, shutil
# from app.config.database import get_session
# from app.modules.incidentes.dto.incidentes_dto import IncidenteCreate, IncidenteRead
# from app.modules.incidentes.services.incidentes_service import IncidenteService
# from app.modules.incidentes.services import services_auth as auth_svc  # get_current_user

# router = APIRouter(prefix="/incidentes", tags=["incidentes"])

# MEDIA_DIR = os.getenv("MEDIA_DIR", "uploads")
# os.makedirs(MEDIA_DIR, exist_ok=True)

# @router.post("/", response_model=IncidenteRead, status_code=status.HTTP_201_CREATED)
# def create_incidente_endpoint(incidente: IncidenteCreate, db: Session = Depends(get_session), current_user = Depends(auth_svc.get_current_user)):
#     svc = IncidenteService(db)
#     try:
#         creado = svc.create_incidente(incidente, creado_por_persona_id=getattr(current_user, "id_persona", None))
#         return creado
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Error interno")

# @router.post("/{id_incidente}/adjuntos/")
# def upload_adjunto(id_incidente: int, file: UploadFile = File(...), db: Session = Depends(get_session), current_user = Depends(auth_svc.get_current_user)):
#     svc = IncidenteService(db)
#     inc = svc.repo.get(id_incidente)
#     if not inc:
#         raise HTTPException(status_code=404, detail="Incidente no encontrado")
#     filename = file.filename
#     dest_path = os.path.join(MEDIA_DIR, f"{id_incidente}_{filename}")
#     with open(dest_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#     adj = svc.upload_adjunto(id_incidente, filename, dest_path, file.content_type, subido_por=getattr(current_user, "id_persona", None))
#     return {"ok": True, "adjunto_id": getattr(adj, "id_adjunto", None)}
