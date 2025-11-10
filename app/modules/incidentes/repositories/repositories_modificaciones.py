# app/modules/incidentes/repositories/repositories_modificaciones.py
from typing import List, Optional
from sqlalchemy.orm import Session

from app.modules.incidentes.repositories.repositories_incidentes import IncidenteRepository
from app.modules.incidentes.models.models_incidentes import Incidente, Estudiante, SituacionIncidente, HistorialDeModificacion

class ModificacionesRepository:
    """
    Repositorio específico para modificaciones, apoyándose en IncidenteRepository
    para operaciones comunes.
    """
    def __init__(self, db: Session):
        self.db = db
        self.base_repo = IncidenteRepository(db)

    def get_incidente(self, id_incidente: int) -> Optional[Incidente]:
        return self.base_repo.get(id_incidente)

    def get_estudiantes_by_ids(self, ids: List[int]) -> List[Estudiante]:
        return self.base_repo.get_estudiantes_by_ids(ids)

    def get_situaciones_by_ids(self, ids: List[int]) -> List[SituacionIncidente]:
        return self.base_repo.get_situaciones_by_ids(ids)

    def save_incidente(self, incidente: Incidente) -> Incidente:
        # incidente es instancia ligada al Session; sólo commit y refresh
        self.db.add(incidente)
        self.db.commit()
        self.db.refresh(incidente)
        return incidente

    def create_historial(self, id_incidente: int, id_persona: Optional[int], campo_modificado: str, valor_anterior: Optional[str], valor_nuevo: Optional[str]) -> HistorialDeModificacion:
        # reutiliza método de IncidenteRepository si existe, si no crear acá
        return self.base_repo.create_historial(id_incidente, id_persona, campo_modificado, valor_anterior, valor_nuevo)
