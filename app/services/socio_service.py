import random
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.socio_repository import SocioRepository
from app.schemas.socio_schema import SocioCreate
from app.models.socio import Socio

class SocioService:
    def __init__(self, db: Session):
        self.repo = SocioRepository(db)

    def crear_socio_con_cuenta(self, socio_data: SocioCreate) -> Socio:
        # 1. Regla de negocio: Validar si el socio ya existe
        socio_existente = self.repo.buscar_por_cedula(socio_data.cedula)
        if socio_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El socio con cédula {socio_data.cedula} ya se encuentra registrado."
            )
        
        # 2. Registrar la información del Socio
        nuevo_socio = self.repo.registrar_socio(socio_data)
        
        # 3. Vincular de manera automática su cuenta de Ahorros inicial (REQ-F-02) 
        # Generamos un número de cuenta aleatorio de 10 dígitos para este ejemplo
        numero_cuenta_random = "".join([str(random.randint(0, 9)) for _ in range(10)])
        self.repo.vincular_cuenta(
            id_socio=nuevo_socio.id_socio,
            numero_cuenta=f"CTA-{numero_cuenta_random}",
            tipo_cuenta="Ahorro"
        )
        
        return nuevo_socio