from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import SessionLocal
from database.models import Vehiculo, Dispositivo
import asyncio
import logging
from typing import List
from math import radians, cos, sin, sqrt, atan2

router = APIRouter()
logger = logging.getLogger(__name__)

# 📌 Lista de conexiones WebSocket activas
conexiones_activas: List[WebSocket] = []
ultima_ubicacion_enviada = {}  # 🔥 Guardar última ubicación enviada por cada vehículo

# ✅ Obtener la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 📡 **WebSocket para enviar ubicación en tiempo real**
@router.websocket("/ws/ubicacion")
async def websocket_ubicacion(websocket: WebSocket):
    await websocket.accept()
    conexiones_activas.append(websocket)
    logger.info("🟢 Cliente conectado al WebSocket de ubicación")

    try:
        # ✅ Enviar mensaje de estado solo al conectar
        await websocket.send_json({"status": "WebSocket activo"})

        while True:
            # 🔍 Obtener vehículos con ubicación
            db: Session = SessionLocal()
            vehiculos = db.query(Vehiculo).filter(Vehiculo.ubicacion.isnot(None)).all()
            db.close()

            if not vehiculos:
                logger.info("⚠️ No hay vehículos con ubicación registrada.")
            else:
                ubicaciones_actualizadas = []
                for v in vehiculos:
                    if v.placa not in ultima_ubicacion_enviada or ultima_ubicacion_enviada[v.placa] != v.ubicacion:
                        ubicaciones_actualizadas.append({
                            "placa": v.placa,
                            "ubicacion": v.ubicacion,
                            "tid": v.tid
                        })
                        ultima_ubicacion_enviada[v.placa] = v.ubicacion  

                if ubicaciones_actualizadas:
                    logger.info(f"📡 Enviando datos WebSocket: {ubicaciones_actualizadas}")
                    for conexion in conexiones_activas[:]:
                        try:
                            await conexion.send_json(ubicaciones_actualizadas)
                        except Exception as e:
                            logger.warning(f"⚠️ Error enviando datos a WebSocket: {e}")
                            conexiones_activas.remove(conexion)

            await asyncio.sleep(3)  

    except WebSocketDisconnect:
        conexiones_activas.remove(websocket)
        logger.info("❌ Cliente desconectado del WebSocket de ubicación")

    except Exception as e:
        logger.error(f"❌ Error en WebSocket: {e}")

    finally:
        if websocket in conexiones_activas:
            conexiones_activas.remove(websocket)
        logger.info("🛑 Cerrando conexión WebSocket")


# 📡 **Función para enviar actualizaciones de ubicación a los clientes WebSocket**
async def notificar_clientes_websocket(ubicacion_data):
    for conexion in conexiones_activas[:]:
        try:
            await conexion.send_json(ubicacion_data)
        except Exception as e:
            logger.warning(f"⚠️ Error enviando datos a WebSocket: {e}")
            conexiones_activas.remove(conexion)

# 📡 **Recibir ubicación desde OwnTracks**
@router.post("/ubicacion")
async def recibir_ubicacion(request: Request, db: Session = Depends(get_db)):
    try:
        body = await request.body()
        if not body:
            logger.warning("⚠️ Se recibió una solicitud vacía en /api/ubicacion")
            raise HTTPException(status_code=400, detail="Solicitud vacía")

        data = await request.json()
        logger.info(f"📡 Datos recibidos: {data}")

        if data.get("_type") not in {"location", "transition", "waypoint"}:
            logger.info(f"🔍 Ignorado mensaje de tipo {data.get('_type')}")
            return {"message": f"Mensaje de tipo {data.get('_type')} ignorado."}

        tid = data.get("tid")
        latitud, longitud = data.get("lat"), data.get("lon")

        if not tid or latitud is None or longitud is None:
            logger.warning(f"⚠️ Faltan datos requeridos: tid={tid}, lat={latitud}, lon={longitud}")
            raise HTTPException(status_code=400, detail="Faltan datos requeridos")

        nueva_ubicacion = f"{latitud},{longitud}"

        vehiculo = db.query(Vehiculo).filter(Vehiculo.tid == tid).first()
        if vehiculo:
            vehiculo.ubicacion = nueva_ubicacion
            db.commit()
            logger.info(f"✅ Ubicación actualizada: {vehiculo.placa} → {nueva_ubicacion}")

            # Notificar WebSocket
            await notificar_clientes_websocket([{
                "placa": vehiculo.placa,
                "ubicacion": nueva_ubicacion,
                "tid": tid
            }])
        else:
            logger.warning(f"⚠️ No se encontró vehículo con TID: {tid}")

        return {"message": "Ubicación procesada correctamente"}

    except Exception as e:
        logger.error(f"❌ Error procesando la ubicación: {e}")
        raise HTTPException(status_code=500, detail="Error procesando la ubicación")

