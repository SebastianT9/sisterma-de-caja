from sqlalchemy import Column, Integer, DECIMAL, Date, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class TablaAmortizacion(Base):
    __tablename__ = "tablas_amortizacion"

    id_cuota = Column(Integer, primary_key=True, index=True)  # PK [cite: 216]
    id_credito = Column(Integer, ForeignKey("creditos.id_credito"), nullable=False)  # FK [cite: 217]
    numero_cuota = Column(Integer, nullable=False)  # INT [cite: 218]
    monto_cuota = Column(DECIMAL(10, 2), nullable=False)  # DECIMAL(10,2) [cite: 219]
    fecha_vencimiento = Column(Date, nullable=False)  # DATE [cite: 219]
    estado_pago = Column(String(20), default="Pendiente")  # VARCHAR(20) [cite: 219]

    # Relación inversa hacia Crédito
    credito = relationship("Credito", back_populates="cuotas")