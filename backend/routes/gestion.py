from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from database import SessionLocal
from services.gestion import Gestion
from schemas.vehiculos import VehiculoCreate, VehiculoUpdate, VehiculoResponse, VehiculoRead
from database.models import Ruta, Vehiculo
from datetime import datetime, timezone
import logging
from sqlalchemy import inspect



# Configuración del logger
logger = logging.getLogger(__name__)

router = APIRouter()

# Dependencia para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🚗 Agregar un vehículo
@router.post("/vehiculos/", response_model=VehiculoRead)
def agregar_vehiculo(vehiculo_data: VehiculoCreate, db: Session = Depends(get_db)):
    gestion = Gestion(db)
    return gestion.agregar_vehiculo(vehiculo_data)


# 🗑️ Eliminar un vehículo
@router.delete("/vehiculos/{id_vehiculo}")
def eliminar_vehiculo(id_vehiculo: int, db: Session = Depends(get_db)):
    gestion = Gestion(db)
    resultado = gestion.eliminar_vehiculo(id_vehiculo)
    if "error" in resultado:
        raise HTTPException(status_code=404, detail=resultado["error"])
    return resultado

# 📋 Listar todos los vehículos
@router.get("/vehiculos/", response_model=List[VehiculoResponse])
def listar_vehiculos(db: Session = Depends(get_db)):
    return db.query(Vehiculo).all()

# 🚙 Obtener vehículos disponibles
@router.get("/vehiculos/disponibles/")
def vehiculos_disponibles(db: Session = Depends(get_db)):
    gestion = Gestion(db)
    return gestion.vehiculo_disponible()

# 🔄 Actualizar un vehículo
@router.put("/vehiculos/{id_vehiculo}")
def actualizar_vehiculo(id_vehiculo: int, vehiculo_data: VehiculoUpdate, db: Session = Depends(get_db)):
    gestion = Gestion(db)
    resultado = gestion.actualizar_vehiculo(id_vehiculo, vehiculo_data)
    if "error" in resultado:
        raise HTTPException(status_code=404, detail=resultado["error"])
    return resultado

# 👷 Asignar un operario a un vehículo
@router.put("/vehiculos/{id_vehiculo}/asignar_operario/")
def asignar_operario(id_vehiculo: int, operario: str, db: Session = Depends(get_db)):
    try:
        gestion = Gestion(db)
        mensaje = gestion.asignar_operario(id_vehiculo, operario)
        return {"message": mensaje}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor.")

# 🛣️ Asignar una ruta a un vehículo
@router.put("/rutas/{id_ruta}/asignar/{id_vehiculo}", response_model=dict)
def asignar_ruta_a_vehiculo(id_ruta: int, id_vehiculo: int, db: Session = Depends(get_db)):
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id_vehiculo == id_vehiculo).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    
    if vehiculo.estado != "disponible":
        raise HTTPException(status_code=400, detail="El vehículo no está disponible para asignar una ruta")

    ruta = db.query(Ruta).filter(Ruta.id_ruta == id_ruta).first()
    if not ruta:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")

    vehiculo.estado = "en uso"
    vehiculo.ubicacion = ruta.origen  # Opcional: inicializar ubicación en el origen de la ruta
    db.add(vehiculo)
    db.commit()
    db.refresh(vehiculo)

    return {"message": f"La ruta {id_ruta} ha sido asignada al vehículo {id_vehiculo}"}

# 📊 Generar un reporte de vehículos
@router.get("/vehiculos/reporte/")
def generar_reporte(db: Session = Depends(get_db)):
    gestion = Gestion(db)
    return gestion.generar_reporte()
