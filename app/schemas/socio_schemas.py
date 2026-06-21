from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional

# Esquema base para Cuentas anidadas en respuestas
class CuentaSchema(BaseModel):
    id_cuenta: int
    numero_cuenta: str
    tipo_cuenta: str
    saldo_actual: float

    class Config:
        from_attributes = True  # Permite leer modelos de SQLAlchemy directamente

# DTO de entrada para registrar un Socio (REQ-F-02) 
class SocioCreate(BaseModel):
    cedula: str = Field(..., min_length=10, max_length=10, description="Cédula de identidad del socio")
    nombre: str = Field(..., min_length=3, max_length=100)
    correo: EmailStr

# DTO de salida para las respuestas HTTP
class SocioResponse(BaseModel):
    id_socio: int
    cedula: str
    nombre: str
    correo: str
    fecha_registro: datetime
    cuentas: List[CuentaSchema] = []

    class Config:
        from_attributes = True

# DTO que representa un movimiento individual en la consulta
class MovimientoDTO(BaseModel):
    id_transaccion: int
    tipo_movimiento: str
    monto: float
    fecha_transaccion: datetime

    class Config:
        from_attributes = True

# DTO de salida para la respuesta del Servicio Web (REQ-F-04)
class ConsultaMovimientosResponse(BaseModel):
    cedula: str
    numero_cuenta: str
    saldo_actual: float
    ultimos_movimientos: List[MovimientoDTO]