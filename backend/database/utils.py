from sqlalchemy.orm import Session
import logging

# Configuración del logger
logger = logging.getLogger(__name__)

def cerrar_sesiones_huerfanas(db: Session):
    """
    Cierra sesiones de base de datos abiertas que no fueron cerradas correctamente.
    """
    try:
        if db.is_active:  # 🔥 Verifica si la sesión tiene una transacción activa
            logger.warning("⚠️ Se detectó una sesión abierta sin cerrar. Realizando rollback antes de continuar.")
            db.rollback()
    except Exception as e:
        logger.error(f"❌ Error al cerrar sesiones huérfanas: {e}")
