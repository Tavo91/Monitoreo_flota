from datetime import datetime, timezone
from sqlalchemy.orm import Session
from database.models import Vehiculo
from threading import Thread
import time
from .models import Vehiculo
import random
from database.__init__ import SessionLocal
# Crear un nuevo vehículo
def crear_vehiculo(db: Session, vehiculo_data: dict):
    try:
        # Si no se especifica la ubicación, asignar una ubicación predeterminada
        vehiculo_data.setdefault("ubicacion", "0.000000,0.000000")
        vehiculo_data.setdefault("ultima_actualizacion", datetime.now(timezone.utc))  # Fecha actual

        # Verificar si ya existe un vehículo con la misma placa
        placa_existente = db.query(Vehiculo).filter(Vehiculo.placa == vehiculo_data["placa"]).first()
        if placa_existente:
            raise ValueError(f"Ya existe un vehículo con la placa {vehiculo_data['placa']}.")
        # Crear el vehículo
        vehiculo = Vehiculo(**vehiculo_data)# Crear el objeto Vehiculo
        db.add(vehiculo)
        db.commit() # Guarda el registro en la base de datos
        db.refresh(vehiculo)# Recarga el objeto para obtener el id_vehiculo generado
        return vehiculo
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error al crear el vehículo: {str(e)}")

# Cambiar el estado del vehículo
def cambiar_estado(db: Session, id_vehiculo: int, nuevo_estado: str):
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id_vehiculo == id_vehiculo).first()
    if not vehiculo:
        return None
    vehiculo.estado = nuevo_estado
    db.commit()
    db.refresh(vehiculo)
    return vehiculo





# Mostrar la información completa del vehículo
def mostrar_informacion(db: Session, id_vehiculo: int):
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id_vehiculo == id_vehiculo).first()
    if not vehiculo:
        return None
    return {
        "id_vehiculo": vehiculo.id_vehiculo,
        "placa": vehiculo.placa,
        "tipo": vehiculo.tipo,
        "modelo": vehiculo.modelo,
        "marca": vehiculo.marca,
        "estado": vehiculo.estado,
        "ubicacion": vehiculo.ubicacion,
        "ultima_actualizacion": vehiculo.ultima_actualizacion,
        "año": vehiculo.año,
        "kilometraje": vehiculo.kilometraje,
        "operario_asignado": vehiculo.operario_asignado,
    }

# Obtener todos los vehículos
def obtener_vehiculos(db: Session):
    return db.query(Vehiculo).all()

# Obtener un vehículo por ID
def obtener_vehiculo_por_id(db: Session, id_vehiculo: int):
    return db.query(Vehiculo).filter(Vehiculo.id_vehiculo == id_vehiculo).first()

# Actualizar un vehículo existente
def actualizar_vehiculo(db: Session, id_vehiculo: int, vehiculo_data: dict):
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id_vehiculo == id_vehiculo).first()
    if not vehiculo:
        return None
    # Verificar si la placa ya existe en otro vehículo
    if "placa" in vehiculo_data:
        placa_existente = db.query(Vehiculo).filter(
            Vehiculo.placa == vehiculo_data["placa"],
            Vehiculo.id_vehiculo != id_vehiculo  # Excluir el vehículo actual
        ).first()
        if placa_existente:
            raise ValueError(f"La placa '{vehiculo_data['placa']}' ya está registrada en otro vehículo.")

    # Actualiza solo los campos proporcionados y conserva los valores existentes
    for key, value in vehiculo_data.items():
        if value is not None:  # Ignorar campos que no están en la solicitud
            setattr(vehiculo, key, value)

    db.commit()
    db.refresh(vehiculo)
    return vehiculo


# Eliminar un vehículo por ID
def eliminar_vehiculo(db: Session, id_vehiculo: int):
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id_vehiculo == id_vehiculo).first()
    if not vehiculo:
        return None
    db.delete(vehiculo)
    db.commit()
    return vehiculo
def __init__(self, vehiculo):
        """
        Inicializa el servicio de Vehículo con la información del vehículo.
        """
        self.vehiculo = vehiculo

def iniciar(self):
        """
        Cambia el estado del vehículo a 'en uso'.
        """
        self.vehiculo.estado = "en uso"
        self.vehiculo.ultima_actualizacion = datetime.now()
        return {"message": f"Vehículo {self.vehiculo.placa} está en uso"}
    
      

def detener(self):
        """
        Cambia el estado del vehículo a 'disponible'.
        """
        self.vehiculo.estado = "disponible"
        self.vehiculo.ultima_actualizacion = datetime.now()
        return {"message": f"Vehículo {self.vehiculo.placa} está disponible"}

def realizar_mantenimiento(self):
        """
        Cambia el estado del vehículo a 'en mantenimiento'.
        """
        self.vehiculo.estado = "en mantenimiento"
        self.vehiculo.ultima_actualizacion = datetime.now()
        return {"message": f"Vehículo {self.vehiculo.placa} está en mantenimiento"}


def estado_actual(self):
        """
        Retorna el estado actual del vehículo.
        """
        return {"placa": self.vehiculo.placa, "estado": self.vehiculo.estado}






