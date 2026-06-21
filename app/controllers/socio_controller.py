from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.schemas.socio_schema import SocioCreate, SocioResponse, ConsultaMovimientosResponse
from app.services.socio_service import SocioService, ConsultaService
from app.config.database import get_db  # Generador de sesiones de base de datos

router = APIRouter()

@router.post(
    "/socios", 
    response_model=SocioResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo socio con su cuenta inicial",
    description="Recibe la información personal del socio, valida que no exista y crea automáticamente una cuenta de ahorros vinculada."
)
def registrar_socio(socio_in: SocioCreate, db: Session = Depends(get_db)):
    servicio = SocioService(db)
    return servicio.crear_socio_con_cuenta(socio_in)

@router.get(
    "/consulta-movimientos",
    response_model=ConsultaMovimientosResponse,
    summary="Servicio Web de Consulta Remota de Socios",
    description="Recibe la cédula y el número de cuenta para retornar el saldo actual y los últimos 3 movimientos contables."
)
def consultar_movimientos(
    cedula: str = Query(..., min_length=10, max_length=10, description="Cédula del socio"),
    numero_cuenta: str = Query(..., description="Número de cuenta individual"),
    db: Session = Depends(get_db)
):
    servicio = ConsultaService(db)
    return servicio.consultar_saldo_y_movimientos(cedula, numero_cuenta)