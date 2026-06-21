from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import date, datetime
from typing import List, Optional

class SolicitudCreditoCreate(BaseModel):
    id_socio: int = Field(..., description="ID del socio que solicita el crédito")
    monto_solicitado: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)

class CuotaAmortizacionResponse(BaseModel):
    numero_cuota: int
    monto_cuota: float
    fecha_vencimiento: date
    estado_pago: str

    class Config:
        from_attributes = True

class CreditoResponse(BaseModel):
    id_credito: int
    id_socio: int
    monto_solicitado: float
    monto_aprobado: float
    estado_credito: str
    cuotas: List[CuotaAmortizacionResponse] = []

    class Config:
        from_attributes = True