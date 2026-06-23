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
    def registrar_pago_cuota(self, pago):        
        # DEBUG TEMPORAL: Imprime lo que recibe para comprobar tipos y valores
        print(f"Buscando cuota -> id_credito: {pago.id_credito} (Tipo: {type(pago.id_credito)}), cuota N°: {pago.numero_cuota} (Tipo: {type(pago.numero_cuota)})")
        
        # Buscamos la cuota asegurando que los tipos coincidan forzando un entero si es necesario
        cuota = self.db.query(TablaAmortizacion).filter(
            TablaAmortizacion.id_credito == int(pago.id_credito),
            TablaAmortizacion.numero_cuota == int(pago.numero_cuota)
        ).first()
        
        # Validación por si el ID de crédito o número de cuota no existen
        if not cuota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"La cuota N° {pago.numero_cuota} para el crédito ID {pago.id_credito} no fue encontrada en el sistema."
            )
            
        # 3. Cambiamos el estado de la cuota a Pagado
        cuota.estado_pago = "Pagado"
        
        # 4. Guardamos los cambios de SQLAlchemy en la base de datos
        try:
            self.db.commit()
            self.db.refresh(cuota)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"Error al confirmar el pago en la base de datos: {str(e)}"
            )
        
        # 5. Retornamos los datos limpios mapeados para el PagoCuotaResponse
        return {
            "id_pago": cuota.id_cuota,  
            "id_credito": cuota.id_credito,
            "numero_cuota": cuota.numero_cuota,
            "monto_pagado": float(pago.monto_pagado),
            "fecha_pago": datetime.utcnow(),  # Recomendado usar utcnow() consistente con tu app
            "estado_cuota_actual": cuota.estado_pago
        }