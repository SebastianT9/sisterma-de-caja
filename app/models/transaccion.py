from sqlalchemy import Column, Integer, String, Decimal, DateTime, ForeignKey
from datetime import datetime
from app.config.database import Base

class TransaccionDiario(Base):
    __tablename__ = "transacciones_diario"

    id_transaccion = Column(Integer, primary_key=True, index=True) # PK [cite: 200]
    id_cuenta = Column(Integer, ForeignKey("cuentas.id_cuenta"), nullable=False) # FK [cite: 201]
    codigo_cuenta_contable = Column(String(50), ForeignKey("plan_cuentas.codigo_cuenta_contable"), nullable=False) # FK [cite: 202]
    tipo_movimiento = Column(String(10), nullable=False) # 'Deposito' o 'Retiro' [cite: 203]
    monto = Column(Decimal(10, 2), nullable=False) # DECIMAL(10,2) [cite: 204]
    fecha_transaccion = Column(DateTime, default=datetime.utcnow) # DATETIME [cite: 205]