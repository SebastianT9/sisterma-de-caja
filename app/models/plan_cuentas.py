from sqlalchemy import Column, String
from app.config.database import Base

class PlanCuentas(Base):
    __tablename__ = "plan_cuentas"

    # Definimos la columna que usas como referencia primaria
    codigo_cuenta_contable = Column(String(50), primary_key=True, index=True)
    nombre_cuenta = Column(String(100), nullable=False)