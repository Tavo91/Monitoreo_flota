from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import traceback
import logging
import uvicorn

from database import models, engine
from routes.ubicacion import router as ubicacion_router
from routes.gestion import router as gestion_router
from routes.vehiculos import router as vehiculos_router
from routes import rutas
from routes import operarios, usuarios
from fastapi.middleware.cors import CORSMiddleware

# 🔥 Configuración de logs para depuración
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    force=True,
)
logger = logging.getLogger(__name__)

# ✅ Inicializar FastAPI
app = FastAPI(docs_url="/docs", redoc_url="/redoc")

# ✅ Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# ✅ Incluir las rutas
app.include_router(ubicacion_router, prefix="/api", tags=["Ubicación"])
app.include_router(usuarios.router, prefix="/api", tags=["Usuarios"])
app.include_router(operarios.router, prefix="/api/operarios", tags=["Operarios"])
app.include_router(vehiculos_router, prefix="/api/vehiculos", tags=["Vehículos"])
app.include_router(gestion_router, prefix="/api/gestion", tags=["Gestión"])
app.include_router(rutas.router, prefix="/api/rutas", tags=["Rutas"])

# ✅ Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Reemplázalo con el dominio de tu frontend en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📌 Ruta raíz para verificar el estado del servidor
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la gestión de flota"}

# 📌 Manejo global de errores para capturar excepciones
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"❌ Error inesperado: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error",
            "error": str(exc),
            "trace": traceback.format_exc()
        }
    )

# 📌 Manejo de errores de validación de FastAPI
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"⚠️ Error de validación: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": exc.body,
        },
    )

# ✅ Ejecutar el servidor si el script es ejecutado directamente
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

