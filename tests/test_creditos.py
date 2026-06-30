import pytest
from app.services.credito_service import CreditoService
from app.repositories.credito_repository import CreditoRepository
from app.schemas.credito_schema import SolicitudCreditoCreate
from app.schemas.credito_schema import PagoCuotaCreate
from decimal import Decimal
from fastapi import HTTPException



def test_aprobar_y_generar_tabla_cuotas_fijas(db_session):
    repo = CreditoRepository(db_session)
    # Crear un crédito inicial en estado 'Solicitado'
    credito_solicitado = repo.crear_solicitud(id_socio=1, monto=Decimal("600.00"))
    
    servicio = CreditoService(db_session)
    credito_procesado = servicio.aprobar_y_generar_tabla(id_credito=credito_solicitado.id_credito, meses_plazo=6)
    
    assert credito_procesado.estado_credito == "Entregado"
    assert len(credito_procesado.cuotas) == 6
    # Validar cuota base: 600 / 6 meses = 100.00 por cuota
    assert credito_procesado.cuotas[0].monto_cuota == Decimal("100.00")
    assert credito_procesado.cuotas[5].numero_cuota == 6

def test_registrar_pago_cuota_no_encontrada(db_session):
    servicio = CreditoService(db_session)
    pago_dto = PagoCuotaCreate(id_credito=999, numero_cuota=1, monto_pagado=Decimal("50.00"))
    
    # El crédito 999 no existe, debe arrojar HTTP 404
    with pytest.raises(HTTPException) as exc_info:
        servicio.registrar_pago_cuota(pago_dto)
        
    assert exc_info.value.status_code == 404
    assert "no fue encontrada en el sistema" in exc_info.value.detail