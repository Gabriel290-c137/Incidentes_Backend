# app/modules/incidentes/services/incidentes_service.py
from typing import Optional
from sqlalchemy.orm import Session
from app.modules.incidentes.models import models_incidentes
from app.modules.incidentes.dto.dto_incidentes import IncidenteCreate
from app.modules.incidentes.repositories.repositories_incidentes import IncidenteRepository

class IncidenteService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = IncidenteRepository(db)

    def create_incidente(self, incidente_in: IncidenteCreate, creado_por_persona_id: Optional[int] = None) -> models_incidentes.Incidente:
        antecedentes_text = incidente_in.antecedentes or ""
        if incidente_in.lugar:
            antecedentes_text = f"Lugar: {incidente_in.lugar}\n{antecedentes_text}".strip()

        acciones_text = incidente_in.acciones_tomadas or ""
        if incidente_in.descripcion:
            acciones_text = f"{incidente_in.descripcion}\n{acciones_text}".strip()

        # Validaciones: estudiantes y situaciones (Pydantic ya obliga, pero chequeamos DB)
        estudiantes = self.repo.get_estudiantes_by_ids(incidente_in.id_estudiantes)
        if len(estudiantes) < 1:
            raise ValueError("No se encontraron estudiantes válidos")
        situaciones = self.repo.get_situaciones_by_ids(incidente_in.id_situaciones)
        if len(situaciones) < 1:
            raise ValueError("No se encontraron situaciones válidas")

        incidente = models_incidentes.Incidente(
            titulo=incidente_in.titulo,
            antecedentes=antecedentes_text or None,
            acciones_tomadas=acciones_text or None,
            seguimiento=incidente_in.seguimiento,
            estado=incidente_in.estado or "provisional",
            creado_por=creado_por_persona_id
            # fecha se asigna por default en el modelo
        )

        incidente.estudiantes = estudiantes
        incidente.situaciones = situaciones

        return self.repo.add(incidente)

    def upload_adjunto(self, id_incidente: int, nombre_archivo: str, ruta: str, tipo_mime: Optional[str] = None, subido_por: Optional[int] = None):
        inc = self.repo.get(id_incidente)
        if not inc:
            raise ValueError("Incidente no encontrado")
        return self.repo.create_adjunto(id_incidente, nombre_archivo, ruta, tipo_mime, subido_por)
