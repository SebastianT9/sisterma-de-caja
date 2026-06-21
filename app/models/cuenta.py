from sqlalchemy import Column, Integer, String, Decimal, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class Cuenta(Base):
    __tablename__ = "cuentas"

    id_cuenta = Column(Integer, primary_key=True, index=True)  # PK [cite: 186]
    id_socio = Column(Integer, ForeignKey("socios.id_socio"), nullable=False)  # FK [cite: 187]
    numero_cuenta = Column(String(20), unique=True, nullable=False, index=True)  # VARCHAR(20) UNIQUE [cite: 191]
    tipo_cuenta = Column(String(20), nullable=False)  # 'Ahorro' o 'Aportacion' [cite: 191]
    saldo_actual = Column(Decimal(10, 2), default=0.00)  # DECIMAL(10,2) [cite: 191]

    # Relación inversa hacia Socio
    socio = relationship("Socio", back_populates="cuentas")