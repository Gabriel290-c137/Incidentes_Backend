# app/modules/incidentes/repositories/repositories_derivaciones.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.incidentes.models.models_derivaciones import Derivacion, Estado
from app.modules.incidentes.models.models_incidentes import Incidente, HistorialDeModificacion
from datetime import datetime

class DerivacionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, id_derivacion: int) -> Optional[Derivacion]:
        return self.db.query(Derivacion).filter(Derivacion.id_derivacion == id_derivacion).first()

    def add(self, derivacion: Derivacion) -> Derivacion:
        self.db.add(derivacion)
        self.db.commit()
        self.db.refresh(derivacion)
        return derivacion

    def list_by_incidente(self, id_incidente: int) -> List[Derivacion]:
        return (
            self.db.query(Derivacion)
            .filter(Derivacion.id_incidente == id_incidente)
            .order_by(Derivacion.fecha_derivacion.desc())
            .all()
        )

    def get_persona(self, id_persona: int):
        # consulta directa a la tabla personas para evitar dependencias circulares
        return self.db.execute(
            "SELECT id_persona, ci, nombres, apellido_paterno, apellido_materno FROM personas WHERE id_persona = :id",
            {"id": id_persona}
        ).first()

    def get_estado_by_id(self, id_estado: int) -> Optional[Estado]:
        return self.db.query(Estado).filter(Estado.id_estado == id_estado).first()

    def get_estado_by_nombre(self, nombre: str) -> Optional[Estado]:
        return self.db.query(Estado).filter(Estado.nombre_estado == nombre).first()

    def update_incidente_estado(self, id_incidente: int, nuevo_estado_nombre: str) -> Optional[Incidente]:
        inc = self.db.query(Incidente).filter(Incidente.id_incidente == id_incidente).first()
        if not inc:
            return None
        inc.estado = nuevo_estado_nombre
        self.db.add(inc)
        self.db.commit()
        self.db.refresh(inc)
        return inc

    def create_historial(self, id_incidente: int, id_persona: Optional[int], campo_modificado: str, valor_anterior: Optional[str], valor_nuevo: Optional[str]):
        h = HistorialDeModificacion(
            id_incidente = id_incidente,
            id_persona = id_persona,
            fecha_cambio = datetime.utcnow(),
            campo_modificado = campo_modificado,
            valor_anterior = valor_anterior,
            valor_nuevo = valor_nuevo
        )
        self.db.add(h)
        self.db.commit()
        self.db.refresh(h)
        return h
