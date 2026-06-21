from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime

# DTO de entrada para procesar un movimiento
class TransaccionCreate(BaseModel):
    numero_cuenta: str = Field(..., description="Número de cuenta del socio")
    monto: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2, description="Monto mayor a cero")
    tipo_movimiento: str = Field(..., description="'Deposito' o 'Retiro'")

# DTO de salida
class TransaccionResponse(BaseModel):
    id_transaccion: int
    numero_cuenta: str
    tipo_movimiento: str
    monto: float
    codigo_cuenta_contable: str
    fecha_transaccion: datetime

    class Config:
        from_attributes = True