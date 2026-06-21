from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.schemas.credito_schema import SolicitudCreditoCreate, CreditoResponse, PagoCuotaCreate, PagoCuotaResponse
from app.services.credito_service import CreditoService
from app.config.database import get_db

router = APIRouter()

@router.post(
    "/creditos/solicitar",
    response_model=CreditoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar solicitud de préstamo",
    description="Inserta un nuevo registro de crédito en estado inicial 'Solicitado'."
)
def solicitar_credito(solicitud: SolicitudCreditoCreate, db: Session = Depends(get_db)):
    servicio = CreditoService(db)
    return servicio.registrar_solicitud(solicitud)

@router.post(
    "/creditos/pagar-cuota",
    response_model=PagoCuotaResponse,
    status_code=status.HTTP_200_OK,
    summary="Registrar pago de cuota",
    description="Registra el abono a una cuota específica del préstamo y recalculación de la tabla de amortización."
)
def registrarPagoCuota(pago: PagoCuotaCreate, db: Session = Depends(get_db)):
    servicio = CreditoService(db)
    return servicio.registrar_pago_cuota(pago)