from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base  # Suponiendo la base declarativa común

class Socio(Base):
    __tablename__ = "socios"

    id_socio = Column(Integer, primary_key=True, index=True)  # PK mapped from DDS [cite: 182]
    cedula = Column(String(10), unique=True, nullable=False, index=True)  # VARCHAR(10) UNIQUE 
    nombre = Column(String(100), nullable=False)  # VARCHAR(100) 
    correo = Column(String(150), nullable=False)  # VARCHAR(150) 
    fecha_registro = Column(DateTime, default=datetime.utcnow)  # DATETIME 

    # Relación 1 a muchos con Cuentas 
    cuentas = relationship("Cuenta", back_populates="socio", cascade="all, delete-orphan")