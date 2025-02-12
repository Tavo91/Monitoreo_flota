from fastapi import HTTPException
from sqlalchemy.orm import Session
from database.models import Vehiculo, Ruta
from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError
from schemas.vehiculos import VehiculoCreate, VehiculoRead, VehiculoUpdate
import logging

# Configurar el logging
logger = logging.getLogger(__name__)

class Gestion:
    def __init__(self, db: Session):
        self.db = db

    # ✅ AGREGAR VEHÍCULO
    def agregar_vehiculo(self, vehiculo_data: VehiculoCreate):
        try:
            logger.info(f"📥 Datos recibidos: {vehiculo_data}")
            logger.info(f"📥 Registrando vehículo: {vehiculo_data}")

            # Verificar si la placa ya existe
            vehiculo_existente = self.db.query(Vehiculo).filter(Vehiculo.placa == vehiculo_data.placa).first()
            if vehiculo_existente:
                raise HTTPException(status_code=400, detail="Ya existe un vehículo con esta placa.")

            # Crear vehículo
            nuevo_vehiculo  = Vehiculo(
                placa=vehiculo_data.placa,
                tipo=vehiculo_data.tipo,
                año=vehiculo_data.año,
                modelo=vehiculo_data.modelo,
                marca=vehiculo_data.marca,
                kilometraje=vehiculo_data.kilometraje,
                ubicacion=vehiculo_data.ubicacion or "0.000000,0.000000",
                ultima_actualizacion=datetime.now(timezone.utc),
                estado=vehiculo_data.estado,
                ultimo_mantenimiento=vehiculo_data.ultimo_mantenimiento,
                consumo_combustible=vehiculo_data.consumo_combustible,
                tid=vehiculo_data.tid  # ✅ Guardamos el TID del dispositivo
            )

            self.db.add(nuevo_vehiculo)
            self.db.commit()
            self.db.refresh(nuevo_vehiculo)

            # 🚀 Registrar qué tipo de objeto es
            logger.info(f"✅ Tipo de vehiculo después de guardar: {type(nuevo_vehiculo)}")

            logger.info(f"✅ Vehículo registrado correctamente con TID: {vehiculo_data.tid}")
            return nuevo_vehiculo

            

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Error en la base de datos: {e}")
            raise HTTPException(status_code=500, detail="Error en la base de datos.")

        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error inesperado: {e}")
            raise HTTPException(status_code=500, detail="Se produjo un error inesperado.")

    # ✅ ELIMINAR VEHÍCULO
    def eliminar_vehiculo(self, id_vehiculo: int):
        try:
            vehiculo = self.db.query(Vehiculo).filter(Vehiculo.id_vehiculo == id_vehiculo).first()
            if not vehiculo:
                logger.warning(f"❌ Intento de eliminar un vehículo inexistente: {id_vehiculo}")
                raise HTTPException(status_code=404, detail="Vehículo no encontrado")

            if vehiculo.estado in ["en uso", "en mantenimiento"]:
                raise HTTPException(status_code=400, detail="No se puede eliminar el vehículo porque está en uso o en mantenimiento.")

            self.db.delete(vehiculo)
            self.db.commit()
            logger.info(f"🗑️ Vehículo eliminado: {id_vehiculo}")
            return {"message": f"Vehículo {id_vehiculo} eliminado"}

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Error al eliminar vehículo {id_vehiculo}: {e}")
            raise HTTPException(status_code=500, detail="Error en la base de datos.")

    # ✅ BUSCAR VEHÍCULO
    def buscar(self, id_vehiculo: int) -> Optional[Vehiculo]:
        return self.db.query(Vehiculo).filter(Vehiculo.id_vehiculo == id_vehiculo).first()

    # ✅ ACTUALIZAR VEHÍCULO
    def actualizar_vehiculo(self, id_vehiculo: int, vehiculo_data: VehiculoUpdate):
        try:
            vehiculo = self.db.query(Vehiculo).filter(Vehiculo.id_vehiculo == id_vehiculo).first()
            if not vehiculo:
                raise HTTPException(status_code=404, detail="Vehículo no encontrado")

            # Actualizar solo los campos enviados en la solicitud
            for key, value in vehiculo_data.dict(exclude_unset=True).items():
                setattr(vehiculo, key, value)

            self.db.commit()
            self.db.refresh(vehiculo)
            logger.info(f"🔄 Vehículo {id_vehiculo} actualizado con éxito.")
            return {"message": f"Vehículo {id_vehiculo} actualizado"}

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Error al actualizar vehículo {id_vehiculo}: {e}")
            raise HTTPException(status_code=500, detail="Error en la base de datos.")

    # ✅ ASIGNAR VEHÍCULO A RUTA
    def asignar_vehiculo_a_ruta(self, id_vehiculo: int, id_ruta: int):
        try:
            vehiculo = self.db.query(Vehiculo).filter(Vehiculo.id_vehiculo == id_vehiculo).first()
            ruta = self.db.query(Ruta).filter(Ruta.id_ruta == id_ruta).first()

            if not vehiculo:
                raise HTTPException(status_code=404, detail="Vehículo no encontrado")
            if not ruta:
                raise HTTPException(status_code=404, detail="Ruta no encontrada")
            if vehiculo.estado != "disponible":
                raise HTTPException(status_code=400, detail="Vehículo no disponible")

            vehiculo.estado = "en uso"
            vehiculo.ubicacion = ruta.origen
            self.db.commit()
            logger.info(f"🚚 Vehículo {id_vehiculo} asignado a ruta {id_ruta}.")
            return {"message": f"Vehículo {id_vehiculo} asignado a ruta {id_ruta}"}

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Error al asignar vehículo {id_vehiculo} a ruta {id_ruta}: {e}")
            raise HTTPException(status_code=500, detail="Error en la base de datos.")
