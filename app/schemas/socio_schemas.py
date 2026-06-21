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