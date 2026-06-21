from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.credito_repository import CreditoRepository
from app.models.amortizacion import TablaAmortizacion
from app.schemas.credito_schema import SolicitudCreditoCreate
from datetime import datetime, timedelta
from decimal import Decimal

class CreditoService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = CreditoRepository(db)

    def registrar_solicitud(self, datos: SolicitudCreditoCreate):
        return self.repo.crear_solicitud(datos.id_socio, datos.monto_solicitado)

    def aprobar_y_generar_tabla(self, id_credito: int, meses_plazo: int = 6):
        # 1. Recuperar el crédito solicitado
        credito = self.repo.buscar_credito(id_credito)
        if not credito or credito.estado_credito != "Solicitado":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El crédito no existe o no está en estado 'Solicitado'.")

        # 2. Transición de estados lógica (REQ-F-05)
        credito.monto_aprobado = credito.monto_solicitado
        credito.estado_credito = "Entregado"  # Pasa directamente a activo/entregado tras desembolso
        credito.fecha_aprobacion = datetime.utcnow()

        # 3. Generación automática de la Tabla de Amortización (Cálculo de Cuotas Fijas)
        monto_total = Decimal(str(credito.monto_aprobado))
        cuota_base = monto_total / Decimal(str(meses_plazo))
        
        lista_cuotas = []
        fecha_actual = datetime.utcnow().date()

        for i in range(1, meses_plazo + 1):
            # Vencimiento cada 30 días cronológicos
            fecha_vencimiento = fecha_actual + timedelta(days=30 * i)
            
            cuota = TablaAmortizacion(
                id_credito=credito.id_credito,
                numero_cuota=i,
                monto_cuota=cuota_base,
                fecha_vencimiento=fecha_vencimiento,
                estado_pago="AlDia"
            )
            lista_cuotas.append(cuota)

        # 4. Persistir la tabla estructurada
        self.repo.guardar_tabla_amortizacion(lista_cuotas)
        self.db.commit()
        self.db.refresh(credito)
        return credito