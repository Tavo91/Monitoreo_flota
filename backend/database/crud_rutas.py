from sqlalchemy.orm import Session
from database.models import Ruta, Vehiculo

def crear_ruta(db: Session, ruta_data: dict):
    nueva_ruta = Ruta(**ruta_data)
    db.add(nueva_ruta)
    db.commit()
    db.refresh(nueva_ruta)
    return nueva_ruta

def asignar_ruta_a_vehiculo(db: Session, id_ruta: int, id_vehiculo: int):
    ruta = db.query(Ruta).filter(Ruta.id_ruta == id_ruta).first()
    if not ruta:
        return {"error": "Ruta no encontrada"}

    vehiculo = db.query(Vehiculo).filter(Vehiculo.id_vehiculo == id_vehiculo).first()
    if not vehiculo:
        return {"error": "Vehículo no encontrado"}

    if vehiculo.estado != "disponible":
        return {"error": f"El vehículo no está disponible. Estado actual: {vehiculo.estado}"}

    # Asignar ruta al vehículo
    ruta.vehiculo_id = id_vehiculo
    vehiculo.estado = "en uso"
    db.commit()
    db.refresh(ruta)
    db.refresh(vehiculo)
    return {"success": f"Ruta '{ruta.origen} -> {ruta.destino}' asignada al vehículo con placa {vehiculo.placa}"}

def obtener_ruta_por_id(db: Session, ruta_id: int):
    """
    Obtiene una ruta por su ID.

    Args:
        db (Session): Sesión de la base de datos.
        ruta_id (int): ID de la ruta.

    Returns:
        Ruta: Objeto de la ruta si existe, None si no.
    """
    return db.query(Ruta).filter(Ruta.id_ruta == ruta_id).first()

def eliminar_ruta(db: Session, ruta: Ruta):
    """
    Elimina una ruta de la base de datos.

    Args:
        db (Session): Sesión de la base de datos.
        ruta (Ruta): Objeto de la ruta a eliminar.

    Returns:
        None
    """
    db.delete(ruta)
    db.commit()

def actualizar_ruta(db: Session, ruta_id: int, datos_actualizados: dict):
    """
    Actualiza una ruta existente en la base de datos.

    :param db: Sesión de la base de datos.
    :param ruta_id: ID de la ruta a actualizar.
    :param datos_actualizados: Diccionario con los datos actualizados.
    :return: La ruta actualizada.
    :raises: ValueError si la ruta no existe.
    """
    ruta = db.query(Ruta).filter(Ruta.id_ruta == ruta_id).first()

    if not ruta:
        raise ValueError(f"No se encontró la ruta con ID {ruta_id}.")

    for key, value in datos_actualizados.items():
        setattr(ruta, key, value)

    db.commit()
    db.refresh(ruta)
    return ruta