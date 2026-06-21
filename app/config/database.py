from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Definición de la cadena de conexión
# Para desarrollo local rápido se puede usar SQLite. 
# Si usan MariaDB/PostgreSQL en producción, cambian la URL.
SQLALCHEMY_DATABASE_URL = "sqlite:///./sistema_caja.db"
# Para PostgreSQL/MariaDB sería: "postgresql://usuario:password@localhost:5432/db_caja"

# 2. Creación del motor (Engine)
# 'check_same_thread' solo es necesario para SQLite
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. Configuración de la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Clase base para que hereden los modelos (Socio, Cuenta, Transaccion, Credito)
Base = declarative_base()

# 5. Dependencia (Yield) para inyectar la sesión en los controladores de FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()