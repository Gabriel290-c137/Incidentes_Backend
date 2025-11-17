# app/modules/incidentes/services/services_incidentes.py
from typing import Optional
from sqlalchemy.orm import Session
from app.modules.incidentes.models import models_incidentes as models
from app.modules.incidentes.dto.dto_incidentes import IncidenteCreate
from app.modules.incidentes.repositories.repositories_incidentes import IncidenteRepository
from app.modules.incidentes.dto.dto_incidentes import IncidenteUpdate
from datetime import datetime
from typing import Optional, List
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
            estado = "abierto"
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


    def get_all_incidentes(self) -> List[models.Incidente]:
        return self.repo.get_all()
    

    def update_incidente(
        self,
        id_incidente: int,
        update_data: IncidenteUpdate,
        modificador_persona_id: Optional[int] = None
    ) -> models.Incidente:
        incidente = self.repo.get(id_incidente)
        if not incidente:
            raise ValueError("Incidente no encontrado")

        cambios = {}

        # --- Actualizar campos de texto ---
        if update_data.antecedentes is not None:
            cambios["antecedentes"] = {
                "anterior": incidente.antecedentes,
                "nuevo": update_data.antecedentes
            }
            incidente.antecedentes = update_data.antecedentes

        if update_data.acciones_tomadas is not None:
            cambios["acciones_tomadas"] = {
                "anterior": incidente.acciones_tomadas,
                "nuevo": update_data.acciones_tomadas
            }
            incidente.acciones_tomadas = update_data.acciones_tomadas

        if update_data.seguimiento is not None:
            cambios["seguimiento"] = {
                "anterior": incidente.seguimiento,
                "nuevo": update_data.seguimiento
            }
            incidente.seguimiento = update_data.seguimiento

        # --- Actualizar estudiantes ---
        if update_data.id_estudiantes is not None:
            estudiantes = self.repo.get_estudiantes_by_ids(update_data.id_estudiantes)
            if len(estudiantes) != len(update_data.id_estudiantes):
                raise ValueError("Uno o más estudiantes no existen")
            cambios["estudiantes"] = {
                "anterior": [e.id_estudiante for e in incidente.estudiantes],
                "nuevo": update_data.id_estudiantes
            }
            incidente.estudiantes = estudiantes

        # --- Actualizar situaciones ---
        if update_data.id_situaciones is not None:
            situaciones = self.repo.get_situaciones_by_ids(update_data.id_situaciones)
            if len(situaciones) != len(update_data.id_situaciones):
                raise ValueError("Una o más situaciones no existen")
            cambios["situaciones"] = {
                "anterior": [s.id_situacion for s in incidente.situaciones],
                "nuevo": update_data.id_situaciones
            }
            incidente.situaciones = situaciones

        # --- Actualizar estado (solo permitir "cerrado") ---
        if update_data.estado is not None:
            if update_data.estado not in ["cerrado"]:
                raise ValueError("Solo se permite cerrar el incidente (estado='cerrado')")
            if incidente.estado == "cerrado":
                raise ValueError("El incidente ya está cerrado")
            
            cambios["estado"] = {
                "anterior": incidente.estado,
                "nuevo": update_data.estado
            }
            incidente.estado = update_data.estado

        # --- Guardar cambios ---
        self.db.commit()
        self.db.refresh(incidente)

        # --- Registrar historial ---
        for campo, valores in cambios.items():
            try:
                self.repo.create_historial(
                    id_incidente=id_incidente,
                    id_persona=modificador_persona_id,
                    campo_modificado=campo,
                    valor_anterior=json.dumps(valores["anterior"], ensure_ascii=False) if valores["anterior"] is not None else None,
                    valor_nuevo=json.dumps(valores["nuevo"], ensure_ascii=False)
                )
            except Exception as e:
                print(f"Error al registrar historial para {campo}: {e}")

        return incidente