from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.transaccion_repository import TransaccionRepository
from app.schemas.transaccion_schema import TransaccionCreate
from decimal import Decimal

class TransaccionService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = TransaccionRepository(db)

    def procesar_transaccion(self, tx_data: TransaccionCreate):
        # 1. Verificar existencia de la cuenta
        cuenta = self.repo.buscar_cuenta_por_numero(tx_data.numero_cuenta)
        if not cuenta:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada.")

        monto_decimal = Decimal(str(tx_data.monto))
        saldo_actual_decimal = Decimal(str(cuenta.saldo_actual))

        # 2. Determinar lógica financiera e identificar Cuenta Contable (REQ-F-06)
        if tx_data.tipo_movimiento.lower() == "deposito":
            nuevo_saldo = saldo_actual_decimal + monto_decimal
            # Ejemplo: Código contable asignado a ingresos por depósitos en efectivo
            codigo_contable = "101.01.01" 
        
        elif tx_data.tipo_movimiento.lower() == "retiro":
            if saldo_actual_decimal < monto_decimal:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Saldo insuficiente para realizar el retiro.")
            nuevo_saldo = saldo_actual_decimal - monto_decimal
            # Ejemplo: Código contable asignado a egresos de caja
            codigo_contable = "101.01.02" 
        
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de movimiento inválido. Use 'Deposito' o 'Retiro'.")

        try:
            # 3. Aplicar cambios de saldo en tiempo real (REQ-F-03)
            self.repo.actualizar_saldo_cuenta(cuenta, nuevo_saldo)

            # 4. Asentar automáticamente en el Libro Diario (REQ-F-06)
            asiento = self.repo.registrar_asiento_diario(
                id_cuenta=cuenta.id_cuenta,
                codigo_contable=codigo_contable,
                tipo=tx_data.tipo_movimiento,
                monto=monto_decimal
            )
            
            # Confirmación de la transacción unificada (Atomicidad)
            self.db.commit()
            self.db.refresh(asiento)

            # Mapear respuesta manual para incluir el número de cuenta plano
            return {
                "id_transaccion": asiento.id_transaccion,
                "numero_cuenta": cuenta.numero_cuenta,
                "tipo_movimiento": asiento.tipo_movimiento,
                "monto": float(asiento.monto),
                "codigo_cuenta_contable": asiento.codigo_cuenta_contable,
                "fecha_transaccion": asiento.fecha_transaccion
            }

        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error crítico al procesar la transacción bancaria.")