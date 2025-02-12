from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import crud_rutas
from database.__init__ import SessionLocal
from schemas.rutas import RutaCreate, RutaRead, RutaUpdate
from database.models import Ruta
from database.models import Vehiculo
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
    Endpoint para crear una nueva ruta.
"""
@router.post("/", response_model=RutaRead)
def crear_ruta(ruta_data: RutaCreate, db: Session = Depends(get_db)):
    try:
        nueva_ruta = crud_rutas.crear_ruta(db, ruta_data.dict())
        return nueva_ruta
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

"""
    Asigna una ruta a un vehículo si el vehículo está disponible y no está en mantenimiento.
"""
"""@router.put("/{id_ruta}/asignar/{id_vehiculo}", response_model=dict)
def asignar_ruta_a_vehiculo(id_ruta: int, id_vehiculo: int, db: Session = Depends(get_db)):
   
    # Obtener el vehículo
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id_vehiculo == id_vehiculo).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    
    if vehiculo.estado != "disponible":
        raise HTTPException(status_code=400, detail="El vehículo no está disponible para asignar una ruta")

    # Obtener la ruta
    ruta = db.query(Ruta).filter(Ruta.id_ruta == id_ruta).first()
    if not ruta:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    
    # Actualizar el estado del vehículo y asignar la ruta
    vehiculo.estado = "en uso"
    vehiculo.ubicacion = ruta.origen  # Opcional: puedes usar esto para inicializar la ubicación del vehículo en el origen de la ruta
    db.add(vehiculo)

    # Opcional: asignar el vehículo a la ruta si lo tienes modelado en la base de datos
    # ruta.vehiculo_asignado = id_vehiculo
    # db.add(ruta)

    db.commit()
    db.refresh(vehiculo)

    return {"message": f"La ruta {id_ruta} ha sido asignada al vehículo {id_vehiculo}"}"""

@router.get("/", response_model=list[RutaRead])
def listar_rutas(db: Session = Depends(get_db)):
    """
    Lista todas las rutas.
    """
    rutas = db.query(Ruta).all()
    return rutas

@router.delete("/{ruta_id}/", status_code=200)
def eliminar_ruta(ruta_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para eliminar una ruta específica.

    Args:
        ruta_id (int): ID de la ruta a eliminar.
        db (Session): Sesión de la base de datos proporcionada por FastAPI.

    Returns:
        dict: Mensaje confirmando la eliminación exitosa.

    Raises:
        HTTPException: Si la ruta no existe o si ocurre un error durante la eliminación.
    """
    try:
        # Verificar si la ruta existe
        ruta = crud_rutas.obtener_ruta_por_id(db, ruta_id)
        if not ruta:
            raise HTTPException(status_code=404, detail=f"Ruta con ID {ruta_id} no encontrada.")
        
        # Eliminar la ruta
        crud_rutas.eliminar_ruta(db, ruta)
        return {"message": f"Ruta con ID {ruta_id} eliminada exitosamente."}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor.")
    
@router.put("/{ruta_id}", response_model=RutaRead)
def actualizar_ruta(ruta_id: int, ruta_data: RutaUpdate, db: Session = Depends(get_db)):
    """
    Actualiza una ruta existente en la base de datos.

    :param ruta_id: ID de la ruta a actualizar.
    :param ruta_data: Datos actualizados de la ruta.
    :param db: Sesión de la base de datos.
    :return: La ruta actualizada.
    """
    try:
        ruta_actualizada = crud_rutas.actualizar_ruta(db, ruta_id, ruta_data.dict(exclude_unset=True))
        return ruta_actualizada
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")