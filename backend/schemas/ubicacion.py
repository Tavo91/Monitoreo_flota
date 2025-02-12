from pydantic import BaseModel

class UbicacionUpdate(BaseModel):
    lat: float
    lng: float
