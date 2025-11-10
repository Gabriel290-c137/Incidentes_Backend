# app/modules/__init__
# Incidentes / Bienestar Estudiantil
# from .controllers import router

# app/modules/incidentes/__init__.py
# paquete incidentes — no importamos routers aquí para evitar ciclos.
# app/modules/incidentes/__init__.py
# """
# Paquete de nivel 'incidentes'. Exporta un router combinado que reúne
# los routers de controllers_auth y controllers_incidentes.
# Esto evita problemas de import circular y facilita la inclusión desde run.py.
# """
# from fastapi import APIRouter

# # importa routers concretos
# from app.modules.incidentes.controllers.controllers_auth import router as auth_router

# # controllers_incidentes puede no existir en algún momento; lo intentamos
# try:
#     from app.modules.incidentes.controllers.controllers_incidentes import router as incidentes_router
# except Exception:
#     incidentes_router = None

# router = APIRouter(prefix="/api")  # opcional prefix global para el paquete
# # registramos routers individuales (sin prefix extra)
# router.include_router(auth_router)
# if incidentes_router:
#     router.include_router(incidentes_router)
