# app/modules/incidentes/controllers/controllers_modificaciones.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_session
from app.modules.incidentes.dto.dto_modificaciones import ModificacionUpdate
from app.modules.incidentes.dto.dto_incidentes import IncidenteRead
from app.modules.incidentes.services.services_modificaciones import ModificacionesService

# Cambié prefix y tags para que aparezca en la sección "modificaciones"
router = APIRouter(prefix="/modificaciones", tags=["modificaciones"])

@router.patch("/{id_incidente}/", response_model=IncidenteRead, status_code=status.HTTP_200_OK)
def modificar_incidente_endpoint(
    id_incidente: int,
    modificacion: ModificacionUpdate,
    db: Session = Depends(get_session)
):
    svc = ModificacionesService(db)
    try:
        actualizado = svc.modificar_incidente(id_incidente, modificacion)
        return actualizado
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al intentar modificar incidente")
