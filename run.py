# """
# Punto de entrada principal para la aplicación BRISA Backend
# """

# import os
# import uvicorn
# from app import create_app

# # Obtener configuración del entorno
# config_name = os.environ.get('ENV', 'development')

# # Crear aplicación
# app = create_app(config_name)

# if __name__ == '__main__':
#     # Configuración para desarrollo
#     port = int(os.environ.get('PORT', 8000))
#     reload = os.environ.get('ENV', 'development') == 'development'
    
#     print(f"🚀 Iniciando BRISA Backend API en puerto {port}")
#     print(f"📝 Entorno: {config_name}")
#     print(f"🔧 Auto-reload: {reload}")
#     print(f"🌐 URL: http://localhost:{port}")
#     print(f"📖 Docs: http://localhost:{port}/docs")
#     print(f"❤️  Health Check: http://localhost:{port}/api/health")
    
#     uvicorn.run(
#         "run:app",
#         host='0.0.0.0',
#         port=port,
#         reload=reload,
#         log_level="info"
#     )

# run.py (raíz del proyecto)
import logging
import traceback
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import create_db_and_tables

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="BRISA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    create_db_and_tables()

    # listar rutas registradas (útil para debug: verás si PATCH /incidentes/{id_incidente}/ aparece)
    try:
        print("=== RUTAS REGISTRADAS ===")
        for r in app.routes:
            try:
                methods = ",".join(sorted(r.methods)) if hasattr(r, "methods") and r.methods else ""
                print(f"RUTA: {r.path}  | endpoint={r.name}  | methods={methods}")
            except Exception:
                print(f"RUTA (no estándar): {getattr(r, 'path', str(r))}")
        print("=========================")
    except Exception:
        logger.error("Error listando rutas en startup", exc_info=True)


# IMPORTAR routers concretos (no import en package que cause ciclos)
from app.modules.incidentes.controllers.controllers_auth import router as auth_router

# incidentes
try:
    from app.modules.incidentes.controllers.controllers_incidentes import router as incidentes_router
except Exception as e:
    incidentes_router = None
    logger.error("Fallo import controllers_incidentes: %s", e, exc_info=True)
    traceback.print_exc()

# derivaciones
try:
    from app.modules.incidentes.controllers.controllers_derivaciones import router as derivaciones_router
except Exception as e:
    derivaciones_router = None
    logger.error("Fallo import controllers_derivaciones: %s", e, exc_info=True)
    traceback.print_exc()

# modificaciones
try:
    from app.modules.incidentes.controllers.controllers_modificaciones import router as modificaciones_router
except Exception as e:
    modificaciones_router = None
    logger.error("Fallo import controllers_modificaciones: %s", e, exc_info=True)
    traceback.print_exc()

# incluir routers (mantener orden y evitar re-asignaciones accidentales)
app.include_router(auth_router)

if incidentes_router:
    app.include_router(incidentes_router)
else:
    logger.info("incidentes_router es None, no se añadió")

if derivaciones_router:
    app.include_router(derivaciones_router)
else:
    logger.info("derivaciones_router es None, no se añadió")

if modificaciones_router:
    app.include_router(modificaciones_router)
else:
    logger.info("modificaciones_router es None, no se añadió")
