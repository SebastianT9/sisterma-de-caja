from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.socio_repository import ConsultaRepository

class ConsultaService:
    def __init__(self, db: Session):
        self.repo = ConsultaRepository(db)

    def consultar_saldo_y_movimientos(self, cedula: str, numero_cuenta: str):
        # 1. Validar credenciales de socio y cuenta (coincidencia lógica)
        cuenta = self.repo.verificar_socio_y_cuenta(cedula, numero_cuenta)
        if not cuenta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Los datos proporcionados no coinciden con ningún registro activo."
            )

        # 2. Extraer los últimos 3 movimientos ordenados cronológicamente
        movimientos = self.repo.obtener_ultimos_tres_movimientos(cuenta.id_cuenta)

        # 3. Retornar los datos financieros estructurados conforme al DTO
        return {
            "cedula": cedula,
            "numero_cuenta": cuenta.numero_cuenta,
            "saldo_actual": float(cuenta.saldo_actual),
            "ultimos_movimientos": movimientos
        }