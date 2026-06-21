from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.transaccion_schema import TransaccionCreate, TransaccionResponse
from app.services.transaccion_service import TransaccionService
from app.config.database import get_db

router = APIRouter()

@router.post(
    "/transacciones/deposito",
    response_model=TransaccionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Procesar Depósito",
    description="Registra un movimiento de ingreso en caja, incrementa el saldo de la cuenta e impacta el Libro Diario contable."
)
def procesar_deposito(tx_in: TransaccionCreate, db: Session = Depends(get_db)):
    servicio = TransaccionService(db)
    # Forzamos o validamos que el tipo sea estrictamente Depósito
    tx_in.tipo_movimiento = "Deposito"
    return servicio.procesar_transaccion(tx_in)

@router.post(
    "/transacciones/retiro",
    response_model=TransaccionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Procesar Retiro",
    description="Valida fondos disponibles, registra el egreso de caja, debita de la cuenta e impacta el Libro Diario contable."
)
def procesar_retiro(tx_in: TransaccionCreate, db: Session = Depends(get_db)):
    servicio = TransaccionService(db)
    # Forzamos o validamos que el tipo sea estrictamente Retiro
    tx_in.tipo_movimiento = "Retiro"
    return servicio.procesar_transaccion(tx_in)