from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.utils import cerrar_sesiones_huerfanas  # Importar la función
# Configura la conexión a la base de datos
SQLALCHEMY_DATABASE_URL = "sqlite:///./gestion_flota.db"  # Cambia esto si usas otra base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define la base para los modelos
Base = declarative_base()

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        cerrar_sesiones_huerfanas(db)  # 🔥 Verifica y cierra sesiones huérfanas al iniciar una nueva sesión
        yield db
    finally:
        db.close()