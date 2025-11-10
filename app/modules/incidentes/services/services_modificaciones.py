# app/modules/incidentes/services/services_modificaciones.py
from typing import Optional, List
from sqlalchemy.orm import Session
import json

from app.modules.incidentes.repositories.repositories_modificaciones import ModificacionesRepository
from app.modules.incidentes.dto.dto_modificaciones import ModificacionUpdate
from app.modules.incidentes.models.models_incidentes import Incidente

class ModificacionesService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ModificacionesRepository(db)

    def modificar_incidente(self, id_incidente: int, mod: ModificacionUpdate) -> Incidente:
        inc = self.repo.get_incidente(id_incidente)
        if not inc:
            raise ValueError("Incidente no encontrado")

        cambios_realizados = []  # list of tuples (campo, anterior, nuevo)

        # Campos escalares
        if mod.antecedentes is not None and mod.antecedentes != inc.antecedentes:
            cambios_realizados.append(("antecedentes", inc.antecedentes, mod.antecedentes))
            inc.antecedentes = mod.antecedentes

        if mod.acciones_tomadas is not None and mod.acciones_tomadas != inc.acciones_tomadas:
            cambios_realizados.append(("acciones_tomadas", inc.acciones_tomadas, mod.acciones_tomadas))
            inc.acciones_tomadas = mod.acciones_tomadas

        if mod.seguimiento is not None and mod.seguimiento != inc.seguimiento:
            cambios_realizados.append(("seguimiento", inc.seguimiento, mod.seguimiento))
            inc.seguimiento = mod.seguimiento

        if mod.estado is not None and mod.estado != inc.estado:
            cambios_realizados.append(("estado", inc.estado, mod.estado))
            inc.estado = mod.estado

        # Relación estudiantes (many-to-many)
        if mod.id_estudiantes is not None:
            nuevos_est = self.repo.get_estudiantes_by_ids(mod.id_estudiantes)
            nuevos_ids = sorted([e.id_estudiante for e in nuevos_est])
            prev_ids = sorted([e.id_estudiante for e in inc.estudiantes]) if inc.estudiantes else []
            if nuevos_ids != prev_ids:
                cambios_realizados.append(("id_estudiantes", json.dumps(prev_ids, ensure_ascii=False), json.dumps(nuevos_ids, ensure_ascii=False)))
                inc.estudiantes = nuevos_est

        # Relación situaciones (many-to-many)
        if mod.id_situaciones is not None:
            nuevas_s = self.repo.get_situaciones_by_ids(mod.id_situaciones)
            nuevos_ids_s = sorted([s.id_situacion for s in nuevas_s])
            prev_ids_s = sorted([s.id_situacion for s in inc.situaciones]) if inc.situaciones else []
            if nuevos_ids_s != prev_ids_s:
                cambios_realizados.append(("id_situaciones", json.dumps(prev_ids_s, ensure_ascii=False), json.dumps(nuevos_ids_s, ensure_ascii=False)))
                inc.situaciones = nuevas_s

        # Si no hay cambios, devolver sin tocar historial
        if not cambios_realizados:
            self.db.refresh(inc)
            return inc

        # Guardar incidente
        saved = self.repo.save_incidente(inc)

        # Crear registros de historial por cada campo cambiado
        id_persona = mod.id_persona if getattr(mod, "id_persona", None) else None
        for campo, anterior, nuevo in cambios_realizados:
            try:
                self.repo.create_historial(
                    id_incidente = saved.id_incidente,
                    id_persona = id_persona,
                    campo_modificado = campo,
                    valor_anterior = anterior,
                    valor_nuevo = nuevo
                )
            except Exception:
                # No interrumpir la operación principal si falla el historial
                pass

        self.db.refresh(saved)
        return saved
