from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import crud_vehiculos
from database.__init__ import SessionLocal
from schemas.vehiculos import VehiculoCreate, VehiculoUpdate, VehiculoRead
from services.gestion import Gestion
from database.crud_vehiculos import *  # Importar las funciones necesarias directamente desde crud
from database.models import Vehiculo  # Importar modelos si es necesario
import logging

logger = logging.getLogger(__name__)  # Crear un logger para el módulo actual
router = APIRouter()

# Obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear un nuevo vehículo
@router.post("/api/gestion/vehiculos/", response_model=VehiculoCreate)
def agregar_vehiculo(vehiculo: VehiculoCreate, db: Session = Depends(get_db)):
    gestion = Gestion(db)
    return gestion.agregar_vehiculo(vehiculo)


@router.put("/vehiculos/{placa}/asignar_tid")
async def asignar_tid(placa: str, tid: str, db: Session = Depends(get_db)):
    vehiculo = db.query(Vehiculo).filter(Vehiculo.placa == placa).first()

    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    vehiculo.tid = tid
    db.commit()
    logger.info(f"🔗 Dispositivo {tid} asignado manualmente al vehículo {placa}")
    return {"message": f"Dispositivo {tid} asignado al vehículo {placa}"}

# Obtener todos los vehículos
@router.get("/vehiculos/", response_model=list[VehiculoRead])
def listar_vehiculos(db: Session = Depends(get_db)):
    return crud_vehiculos.obtener_vehiculos(db)

# Obtener un vehículo por ID
@router.get("/vehiculos/{id_vehiculo}", response_model=VehiculoRead)
def obtener_vehiculo(id_vehiculo: int, db: Session = Depends(get_db)):
    vehiculo = crud_vehiculos.obtener_vehiculo_por_id(db, id_vehiculo)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehiculo

#@router.get("/vehiculos/{id_vehiculo}/ubicacion/")
"""def obtener_y_actualizar_ubicacion(id_vehiculo: int, db: Session = Depends(get_db)):
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id_vehiculo == id_vehiculo).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    
    # Generar nueva ubicación aleatoria (simulación)
    nueva_ubicacion = f"{uniform(-90, 90):.6f},{uniform(-180, 180):.6f}"
    vehiculo.ubicacion = nueva_ubicacion
    vehiculo.ultima_actualizacion = datetime.now(timezone.utc)
    db.commit()
    db.refresh(vehiculo)

    return {
        "id_vehiculo": vehiculo.id_vehiculo,
        "ubicacion": vehiculo.ubicacion,
        "ultima_actualizacion": vehiculo.ultima_actualizacion
    }"""
# Actualizar un vehículo
"""@router.put("/vehiculos/{id_vehiculo}", response_model=VehiculoUpdate)
def actualizar_datos_vehiculo(id_vehiculo: int, vehiculo_data: VehiculoUpdate, db: Session = Depends(get_db)):
    vehiculo_actualizado = actualizar_vehiculo(db, id_vehiculo, vehiculo_data.model_dump(exclude_unset=True))
    if not vehiculo_actualizado:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehiculo_actualizado
"""



@router.put("/vehiculos/{id_vehiculo}/iniciar/")
def iniciar_vehiculo(id_vehiculo: int, db: Session = Depends(get_db)):
    vehiculo = crud_vehiculos.cambiar_estado(db, id_vehiculo, "en uso")
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehiculo

@router.put("/vehiculos/{id_vehiculo}/detener/")
def detener_vehiculo(id_vehiculo: int, db: Session = Depends(get_db)):
    vehiculo = crud_vehiculos.cambiar_estado(db, id_vehiculo, "disponible")
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehiculo

@router.put("/vehiculos/{id_vehiculo}/mantenimiento/")
def realizar_mantenimiento(id_vehiculo: int, db: Session = Depends(get_db)):
    vehiculo = crud_vehiculos.cambiar_estado(db, id_vehiculo, "en mantenimiento")
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehiculo

"""@router.put("/{id_vehiculo}/asignar_ruta/{id_ruta}/")
def asignar_ruta(id_vehiculo: int, id_ruta: int, db: Session = Depends(get_db)):
    gestion = Gestion(db)
    return gestion.asignar_vehiculo_a_tarea(id_vehiculo, id_ruta)

"""

"""@router.put("/{id_vehiculo}/asignar_operario/")
def asignar_operario(id_vehiculo: int, operario: str, db: Session = Depends(get_db)):
    gestion = Gestion(db)
    return gestion.asignar_operario(id_vehiculo, operario)
"""

@router.get("/vehiculos/{id_vehiculo}/informacion/")
def mostrar_informacion(id_vehiculo: int, db: Session = Depends(get_db)):
    informacion = crud_vehiculos.mostrar_informacion(db, id_vehiculo)
    if not informacion:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return informacion

@router.get("/disponibles/")
def vehiculos_disponibles(db: Session = Depends(get_db)):
    gestion = Gestion(db)
    return gestion.vehiculo_disponible()

@router.get("/reporte/")
def generar_reporte(db: Session = Depends(get_db)):
    gestion = Gestion(db)
    return gestion.generar_reporte()

# Eliminar un vehículo
@router.delete("/{id_vehiculo}/")
def eliminar_vehiculo(id_vehiculo: int, db: Session = Depends(get_db)):
    gestion = Gestion(db)
    return gestion.eliminar_vehiculo(id_vehiculo)
    





