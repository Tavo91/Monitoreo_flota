from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.usuario import UsuarioCreate, UsuarioLogin, UsuarioRead
from database.crud_usuarios import crear_usuario, autenticar_usuario, obtener_usuarios
from database.models import Usuario

router = APIRouter()

# Crear un nuevo usuario
@router.post("/usuarios/", response_model=UsuarioRead)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.correo == usuario.correo).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    return crear_usuario(db=db, usuario=usuario)

# Inicio de sesión
@router.post("/login/")
def iniciar_sesion(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    usuario_db = autenticar_usuario(db, usuario.correo, usuario.contrasena)
    if not usuario_db:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
    return {
        "message": "Inicio de sesión exitoso",
        "user": {"id": usuario_db.id, "nombre": usuario_db.nombre, "es_admin": usuario_db.es_admin}
    }

@router.get("/usuarios/", response_model=list[UsuarioRead])
def listar_usuarios(db: Session = Depends(get_db)):
    """
    Endpoint para listar todos los usuarios registrados.

    Returns:
        List[UsuarioRead]: Lista de usuarios con sus detalles.
    """
    usuarios = obtener_usuarios(db)
    if not usuarios:
        raise HTTPException(status_code=404, detail="No hay usuarios registrados")
    return usuarios