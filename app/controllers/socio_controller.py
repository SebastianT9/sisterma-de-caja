from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.socio_schema import SocioCreate, SocioResponse
from app.services.socio_service import SocioService
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