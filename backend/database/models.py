from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from database import Base

Base = declarative_base()

class Vehiculo(Base):
    __tablename__ = 'vehiculos'
    id_vehiculo = Column(Integer, primary_key=True, autoincrement=True)  # ID autoincremental
    placa = Column(String, unique=True, nullable=False)
    tipo = Column(String, nullable=False)
    año = Column(Integer, nullable=False)
    modelo = Column(String, nullable=False)
    marca = Column(String, nullable=False)
    kilometraje = Column(Float, nullable=False)
    ubicacion = Column(String, nullable=True, default="0.000000,0.000000")  # Latitud y longitud como string y por defecto
    ultima_actualizacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    estado = Column(String, default="disponible")  # "disponible", "en uso", "en mantenimiento"
    operario_asignado = Column(String, nullable=True)  # Nombre del operario asignado
    ultimo_mantenimiento = Column(Date, nullable=True)
    consumo_combustible = Column(Float, nullable=True)
    tid = Column(String, unique=True, nullable=True)  # 🔥 Nuevo campo para almacenar el TID del dispositivo

    dispositivo = relationship("Dispositivo", back_populates="vehiculo")  # Relación ORM
    ruta = relationship("Ruta", back_populates="vehiculo", uselist=False)  # Relación 1:1 con Ruta

class Ruta(Base):
    __tablename__ = "rutas"

    id_ruta = Column(Integer, primary_key=True, index=True)
    origen = Column(String, nullable=False)
    destino = Column(String, nullable=False)
    distancia = Column(Float, nullable=False)
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id_vehiculo"), nullable=True)  # Relación con Vehiculo

    # Relación con el modelo Vehiculo
    vehiculo = relationship("Vehiculo", back_populates="ruta")


class Dispositivo(Base):
    __tablename__ = "dispositivos"

    tid = Column(String, primary_key=True, index=True)  # ID del dispositivo (Tracker ID)
    modelo = Column(String, nullable=True)
    usuario = Column(String, nullable=True)
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id_vehiculo"), nullable=True)

    vehiculo = relationship("Vehiculo", back_populates="dispositivo")  # Relación ORM
    
class Operario(Base):
    __tablename__ = "operarios"

    id_operario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    telefono = Column(String, nullable=False, unique=True)
    cargo = Column(String, nullable=False)

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False)
    contrasena = Column(String, nullable=False)  # Contraseña encriptada
    es_admin = Column(Boolean, default=False)    # Define si el usuario es administrador

    @property
    def rol(self):
        return "admin" if self.es_admin else "operario"