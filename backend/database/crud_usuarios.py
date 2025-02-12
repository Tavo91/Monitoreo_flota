from sqlalchemy.orm import Session
from database.models import Usuario
from schemas.usuario import UsuarioCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Crear usuario
def crear_usuario(db: Session, usuario: UsuarioCreate):
    hashed_password = pwd_context.hash(usuario.contrasena)
    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        contrasena=hashed_password,
        es_admin=usuario.es_admin
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

# Autenticar usuario
def autenticar_usuario(db: Session, correo: str, contrasena: str):
    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    if not usuario or not pwd_context.verify(contrasena, usuario.contrasena):
        return None
    return usuario

def obtener_usuarios(db: Session):
    """
    Recupera todos los usuarios registrados en la base de datos.

    Args:
        db (Session): Sesión de la base de datos.

    Returns:
        List[Usuario]: Lista de usuarios registrados.
    """
    return db.query(Usuario).all()