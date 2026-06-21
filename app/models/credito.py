from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base

class Credito(Base):
    __tablename__ = "creditos"

    id_credito = Column(Integer, primary_key=True, index=True)  # PK [cite: 210]
    id_socio = Column(Integer, ForeignKey("socios.id_socio"), nullable=False)  # FK [cite: 211]
    monto_solicitado = Column(DECIMAL(10, 2), nullable=False)  # DECIMAL(10,2) [cite: 211]
    monto_aprobado = Column(DECIMAL(10, 2), default=0.00)  # DECIMAL(10,2) [cite: 211]
    estado_credito = Column(String(20), default="Solicitado")  # VARCHAR(20) [cite: 211, 280]
    fecha_aprobacion = Column(DateTime, nullable=True)  # DATETIME [cite: 211]

    # Relación con las cuotas de la tabla de amortización
    cuotas = relationship("TablaAmortizacion", back_populates="credito", cascade="all, delete-orphan")