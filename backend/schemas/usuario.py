from pydantic import BaseModel, EmailStr

# Esquema base
class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr

# Esquema para crear usuario
class UsuarioCreate(UsuarioBase):
    contrasena: str
    es_admin: bool = False

# Esquema para leer usuario
class UsuarioRead(BaseModel):
    id: int
    nombre: str
    correo: EmailStr
    rol: str  # Asegúrate de que el campo rol esté presente en el esquema

    class Config:
        from_attributes = True  # Para convertir ORM a Pydantic

# Esquema para inicio de sesión
class UsuarioLogin(BaseModel):
    correo: EmailStr
    contrasena: str

class UsuarioRead(BaseModel):
    id: int
    nombre: str
    correo: EmailStr
    rol: str

    class Config:
        from_attributes = True  # Permite la conversión de modelos de SQLAlchemy a Pydantic