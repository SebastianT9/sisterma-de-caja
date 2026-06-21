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

class PagoCuotaCreate(BaseModel):
    id_credito: int = Field(..., description="ID del crédito al que pertenece la cuota")
    numero_cuota: int = Field(..., gt=0, description="Número secuencial de la cuota a pagar")
    monto_pagado: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2, description="Monto exacto que se está abonando/pagando")

class PagoCuotaResponse(BaseModel):
    id_pago: int = Field(..., description="ID único del registro de pago")
    id_credito: int
    numero_cuota: int
    monto_pagado: float
    fecha_pago: datetime
    estado_cuota_actual: str = Field(..., description="Nuevo estado de la cuota (ej. 'Pagado', 'Abonado')")

    class Config:
        from_attributes = True