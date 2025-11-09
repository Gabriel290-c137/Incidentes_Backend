# app/modules/incidentes/repositories/incidentes_repository.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.incidentes.models.models_incidentes import Incidente as IncidenteModel, Estudiante, SituacionIncidente, Adjunto

class IncidenteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, id_incidente: int) -> Optional[IncidenteModel]:
        return self.db.query(IncidenteModel).filter(IncidenteModel.id_incidente == id_incidente).first()

    def add(self, incidente: IncidenteModel) -> IncidenteModel:
        self.db.add(incidente)
        self.db.commit()
        self.db.refresh(incidente)
        return incidente

    def get_estudiantes_by_ids(self, ids: List[int]):
        return self.db.query(Estudiante).filter(Estudiante.id_estudiante.in_(ids)).all()

    def get_situaciones_by_ids(self, ids: List[int]):
        return self.db.query(SituacionIncidente).filter(SituacionIncidente.id_situacion.in_(ids)).all()

    def create_adjunto(self, id_incidente: int, nombre_archivo: str, ruta: str, tipo_mime: str = None, subido_por: int = None) -> Adjunto:
        adj = Adjunto(id_incidente=id_incidente, nombre_archivo=nombre_archivo, ruta=ruta, tipo_mime=tipo_mime, subido_por=subido_por)
        self.db.add(adj)
        self.db.commit()
        self.db.refresh(adj)
        return adj
