from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.schemas.credito_schema import SolicitudCreditoCreate, CreditoResponse
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
    "/creditos/{id_credito}/aprobar",
    response_model=CreditoResponse,
    summary="Aprobar crédito y estructurar tabla de amortización",
    description="Cambia el estado del crédito a 'Entregado' y calcula secuencialmente el cronograma de cuotas automáticas."
)
def aprobar_credito(id_credito: int, plazo_meses: int = Query(6, gte=1), db: Session = Depends(get_db)):
    servicio = CreditoService(db)
    return servicio.aprobar_y_generar_tabla(id_credito, plazo_meses)