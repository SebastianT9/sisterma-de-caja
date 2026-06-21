from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.transaccion_schema import TransaccionCreate, TransaccionResponse
from app.services.transaccion_service import TransaccionService
from app.config.database import get_db

router = APIRouter()

@router.post(
    "/transacciones",
    response_model=TransaccionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Procesar Depósitos y Retiros con asiento contable automático",
    description="Registra un movimiento en caja, actualiza los saldos en tiempo real e impacta de forma automática el Libro Diario contable."
)
def ejecutar_transaccion(tx_in: TransaccionCreate, db: Session = Depends(get_db)):
    servicio = TransaccionService(db)
    return servicio.procesar_transaccion(tx_in)