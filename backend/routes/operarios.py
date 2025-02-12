from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import OperarioCreate, OperarioRead, OperarioUpdate
from database import crud_operarios

router = APIRouter(prefix="/api/operarios", tags=["Operarios"])

# Crear un operario
@router.post("/", response_model=OperarioRead)
def crear_operario(operario_data: OperarioCreate, db: Session = Depends(get_db)):
    return crud_operarios.crear_operario(db, operario_data)

# Obtener todos los operarios
@router.get("/", response_model=list[OperarioRead])
def obtener_operarios(db: Session = Depends(get_db)):
    return crud_operarios.obtener_operarios(db)

# Obtener un operario por ID
@router.get("/{operario_id}", response_model=OperarioRead)
def obtener_operario_por_id(operario_id: int, db: Session = Depends(get_db)):
    operario = crud_operarios.obtener_operario_por_id(db, operario_id)
    if not operario:
        raise HTTPException(status_code=404, detail="Operario no encontrado")
    return operario

# Actualizar un operario
@router.put("/{operario_id}", response_model=OperarioRead)
def actualizar_operario(operario_id: int, operario_data: OperarioUpdate, db: Session = Depends(get_db)):
    operario_actualizado = crud_operarios.actualizar_operario(db, operario_id, operario_data)
    if not operario_actualizado:
        raise HTTPException(status_code=404, detail="Operario no encontrado")
    return operario_actualizado

# Eliminar un operario
@router.delete("/{operario_id}", response_model=dict)
def eliminar_operario(operario_id: int, db: Session = Depends(get_db)):
    exito = crud_operarios.eliminar_operario(db, operario_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Operario no encontrado")
    return {"message": "Operario eliminado correctamente"}
