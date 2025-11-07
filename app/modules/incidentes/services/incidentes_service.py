from typing import Optional
from sqlalchemy.orm import Session
from app.modules.incidentes import models
from app.modules.incidentes.dto import IncidenteCreate
from app.modules.incidentes.repositories.incidentes_repository import IncidenteRepository

class IncidenteService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = IncidenteRepository(db)

    def create_incidente(self, incidente_in: IncidenteCreate) -> models.Incidente:
        antecedentes_text = incidente_in.antecedentes or ""
        if incidente_in.lugar:
            antecedentes_text = f"Lugar: {incidente_in.lugar}\n{antecedentes_text}".strip()

        acciones_text = incidente_in.acciones_tomadas or ""
        if incidente_in.descripcion:
            acciones_text = f"{incidente_in.descripcion}\n{acciones_text}".strip()

        incidente = models.Incidente(
            fecha=incidente_in.fecha,
            antecedentes=antecedentes_text or None,
            acciones_tomadas=acciones_text or None,
            seguimiento=incidente_in.seguimiento,
            estado=incidente_in.estado or "provisional",
        )

        if incidente_in.id_estudiantes:
            incidente.estudiantes = self.repo.get_estudiantes_by_ids(incidente_in.id_estudiantes)

        if incidente_in.id_situaciones:
            incidente.situaciones = self.repo.get_situaciones_by_ids(incidente_in.id_situaciones)

        return self.repo.add(incidente)

    def upload_adjunto(self, id_incidente: int, nombre_archivo: str, ruta: str, tipo_mime: Optional[str] = None, subido_por: Optional[int] = None):
        # valida existencia de incidente
        inc = self.repo.get(id_incidente)
        if not inc:
            raise ValueError("Incidente no encontrado")
        return self.repo.create_adjunto(id_incidente, nombre_archivo, ruta, tipo_mime, subido_por)
