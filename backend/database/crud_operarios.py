from sqlalchemy.orm import Session
from .models import Operario
from schemas import OperarioCreate, OperarioUpdate

# Crear un nuevo operario
def crear_operario(db: Session, operario_data: OperarioCreate):
    nuevo_operario = Operario(**operario_data.dict())
    db.add(nuevo_operario)
    db.commit()
    db.refresh(nuevo_operario)
    return nuevo_operario

# Obtener todos los operarios
def obtener_operarios(db: Session):
    return db.query(Operario).all()

# Obtener un operario por ID
def obtener_operario_por_id(db: Session, operario_id: int):
    return db.query(Operario).filter(Operario.id_operario == operario_id).first()

# Actualizar un operario
def actualizar_operario(db: Session, operario_id: int, operario_data: OperarioUpdate):
    operario = db.query(Operario).filter(Operario.id_operario == operario_id).first()
    if not operario:
        return None
    for key, value in operario_data.dict(exclude_unset=True).items():
        setattr(operario, key, value)
    db.commit()
    db.refresh(operario)
    return operario

# Eliminar un operario
def eliminar_operario(db: Session, operario_id: int):
    operario = db.query(Operario).filter(Operario.id_operario == operario_id).first()
    if operario:
        db.delete(operario)
        db.commit()
        return True
    return False
