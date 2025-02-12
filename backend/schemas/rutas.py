from pydantic import BaseModel
from typing import Optional

class RutaCreate(BaseModel):
    origen: str
    destino: str
    distancia: float

class RutaRead(RutaCreate):
    id_ruta: int
    vehiculo_id: int | None = None

    class Config:
        from_attributes = True

class RutaUpdate(BaseModel):
    origen: Optional[str]
    destino: Optional[str]
    distancia: Optional[float]
    vehiculo_id: Optional[int]

    class Config:
        from_attributes = True
