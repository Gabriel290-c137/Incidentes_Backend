# app/modules/incidentes/services/services_incidentes.py
from typing import Optional
from sqlalchemy.orm import Session
from app.modules.incidentes.models import models_incidentes as models
from app.modules.incidentes.dto.dto_incidentes import IncidenteCreate
from app.modules.incidentes.repositories.repositories_incidentes import IncidenteRepository
from datetime import datetime
import json

class IncidenteService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = IncidenteRepository(db)

    def create_incidente(self, incidente_in: IncidenteCreate, creador_persona_id: Optional[int] = None) -> models.Incidente:
        # validar estudiantes
        estudiantes = self.repo.get_estudiantes_by_ids(incidente_in.id_estudiantes)
        if not estudiantes or len(estudiantes) < 1:
            raise ValueError("No se encontraron estudiantes válidos")

        # validar situaciones
        situaciones = self.repo.get_situaciones_by_ids(incidente_in.id_situaciones)
        if not situaciones or len(situaciones) < 1:
            raise ValueError("No se encontraron situaciones válidas")

        incidente = models.Incidente(
            fecha = datetime.utcnow(),
            antecedentes = incidente_in.antecedentes,
            acciones_tomadas = incidente_in.acciones_tomadas,
            seguimiento = incidente_in.seguimiento,
            estado = "provisional"
        )

        incidente.estudiantes = estudiantes
        incidente.situaciones = situaciones

        # guardar incidente primero
        creado = self.repo.add(incidente)

        # luego registrar en historial_de_modificaciones la creación
        valor_nuevo = json.dumps({
            "antecedentes": incidente_in.antecedentes,
            "acciones_tomadas": incidente_in.acciones_tomadas,
            "seguimiento": incidente_in.seguimiento,
            "id_estudiantes": incidente_in.id_estudiantes,
            "id_situaciones": incidente_in.id_situaciones
        }, ensure_ascii=False)

        try:
            self.repo.create_historial(
                id_incidente=creado.id_incidente,
                id_persona=creador_persona_id,
                campo_modificado="creacion",
                valor_anterior=None,
                valor_nuevo=valor_nuevo
            )
        except Exception:
            # si falla el historial, no revertimos el incidente; opcional: registrar/loggear
            pass

        return creado

    def upload_adjunto(self, id_incidente: int, nombre_archivo: str, ruta: str, tipo_mime: Optional[str] = None, subido_por: Optional[int] = None):
        inc = self.repo.get(id_incidente)
        if not inc:
            raise ValueError("Incidente no encontrado")
        return self.repo.create_adjunto(id_incidente, nombre_archivo, ruta, tipo_mime, subido_por)
