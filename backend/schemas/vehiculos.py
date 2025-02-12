from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from typing import Optional



class UbicacionUpdate(BaseModel):
    latitud: float
    longitud: float

    def to_string(self) -> str:
        """Convierte latitud y longitud en una cadena 'lat,long'."""
        return f"{self.latitud},{self.longitud}"


# 🔹 Esquema para CREAR un vehículo
class VehiculoCreate(BaseModel):
    placa: str
    tipo: str
    año: int
    modelo: str
    marca: str
    kilometraje: float
    ubicacion: Optional[str] = "0.000000,0.000000"  
    estado: Optional[str] = "disponible"
    ultimo_mantenimiento: Optional[date] = None
    consumo_combustible: Optional[float] = None
    tid: Optional[str] = None  # 🔥 Nuevo campo para almacenar el ID del dispositivo

    model_config = {"from_attributes": True}  # Adaptado a Pydantic v2


# 🔹 Esquema para ACTUALIZAR un vehículo
class VehiculoUpdate(BaseModel):
    placa: Optional[str] = None
    tipo: Optional[str] = None
    año: Optional[int] = None
    modelo: Optional[str] = None
    marca: Optional[str] = None
    kilometraje: Optional[float] = None
    ubicacion: Optional[str] = None
    estado: Optional[str] = None
    operario_asignado: Optional[str] = None
    consumo_combustible: Optional[float] = None

    model_config = {"from_attributes": True}


# 🔹 Esquema para LEER un vehículo (Datos más básicos)
class VehiculoRead(BaseModel):
    id_vehiculo: int
    placa: str
    tipo: str
    modelo: str
    marca: str
    año: int
    kilometraje: float
    ubicacion: Optional[str]
    estado: str
    operario_asignado: Optional[str] = None
    ultima_actualizacion: Optional[datetime] = None

    model_config = {"from_attributes": True}

    # ✅ Validador para mostrar "No disponible" si la ubicación es nula o inválida
    @field_validator("ubicacion")
    def validar_ubicacion(cls, value):
        if not value or value == "0.000000,0.000000":
            return "No disponible"
        return value

    model_config = {"from_attributes": True}


# 🔹 Esquema de RESPUESTA (Devuelve más datos)
class VehiculoResponse(VehiculoRead):
    consumo_combustible: Optional[float] = None
    ultimo_mantenimiento: Optional[date] = None

    model_config = {"from_attributes": True}


# 🔹 Esquema para ACTUALIZAR UBICACIÓN del vehículo
class UbicacionUpdate(BaseModel):
    ubicacion: str  # Latitud y longitud en formato "lat,long"

    model_config = {"from_attributes": True}
