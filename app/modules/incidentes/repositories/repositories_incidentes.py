# app/modules/incidentes/repositories/repositories_incidentes.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.incidentes.models.models_incidentes import Incidente, Estudiante, SituacionIncidente, Adjunto, HistorialDeModificacion

class IncidenteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, id_incidente: int) -> Optional[Incidente]:
        return self.db.query(Incidente).filter(Incidente.id_incidente == id_incidente).first()

    def add(self, incidente: Incidente) -> Incidente:
        self.db.add(incidente)
        self.db.commit()
        self.db.refresh(incidente)
        return incidente

    def get_estudiantes_by_ids(self, ids: List[int]):
        return self.db.query(Estudiante).filter(Estudiante.id_estudiante.in_(ids)).all()

    def get_situaciones_by_ids(self, ids: List[int]):
        return self.db.query(SituacionIncidente).filter(SituacionIncidente.id_situacion.in_(ids)).all()

    def create_adjunto(self, id_incidente: int, nombre_archivo: str, ruta: str, tipo_mime: str = None, subido_por: int = None) -> Adjunto:
        adj = Adjunto(
            id_incidente=id_incidente,
            nombre_archivo=nombre_archivo,
            ruta=ruta,
            tipo_mime=tipo_mime,
            subido_por=subido_por
        )
        self.db.add(adj)
        self.db.commit()
        self.db.refresh(adj)
        return adj

    def create_historial(self, id_incidente: int, id_persona: Optional[int], campo_modificado: str, valor_anterior: Optional[str], valor_nuevo: Optional[str]) -> HistorialDeModificacion:
        h = HistorialDeModificacion(
            id_incidente = id_incidente,
            id_persona = id_persona,
            campo_modificado = campo_modificado,
            valor_anterior = valor_anterior,
            valor_nuevo = valor_nuevo
        )
        self.db.add(h)
        self.db.commit()
        self.db.refresh(h)
        return h


    def get_all(self) -> List[Incidente]:
        return self.db.query(Incidente).order_by(Incidente.fecha.desc()).all()