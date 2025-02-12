from pydantic import BaseModel
from typing import Optional

# Esquema para crear un Operario
class OperarioCreate(BaseModel):
    nombre: str
    apellido: str
    telefono: str
    cargo: str

# Esquema para leer un Operario (respuesta)
class OperarioRead(OperarioCreate):
    id_operario: int

    class Config:
        from_attributes = True  # Reemplaza orm_mode

# Esquema para actualizar un Operario
class OperarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    cargo: Optional[str] = None
