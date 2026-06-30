import pytest
from fastapi import HTTPException
from app.services.socio_service import SocioService
from app.schemas.socio_schemas import SocioCreate 
from app.services.consulta_service import ConsultaService

def test_crear_socio_con_cuenta_exito(db_session):
    servicio = SocioService(db_session)
    datos_socio = SocioCreate(cedula="1726354728", nombre="Juan Perez", correo="juan.perez@test.com")
    
    socio_creado = servicio.crear_socio_con_cuenta(datos_socio)
    
    assert socio_creado.id_socio is not None
    assert socio_creado.cedula == "1726354728"
    assert len(socio_creado.cuentas) == 1
    assert socio_creado.cuentas[0].numero_cuenta.startswith("CTA-")

def test_crear_socio_duplicado_lanza_error(db_session):
    servicio = SocioService(db_session)
    datos_socio = SocioCreate(cedula="1726354728", nombre="Juan Perez", correo="juan.perez@test.com")
    
    # Guardamos el primero
    servicio.crear_socio_con_cuenta(datos_socio)
    
    # Intentamos guardar el segundo con la misma cédula
    with pytest.raises(HTTPException) as exc_info:
        servicio.crear_socio_con_cuenta(datos_socio)
        
    assert exc_info.value.status_code == 400
    assert "ya se encuentra registrado" in exc_info.value.detail

def test_consultar_saldo_y_movimientos_error_credenciales(db_session):
    servicio_consulta = ConsultaService(db_session)
    
    # Buscar una cuenta inexistente debe arrojar HTTP 404
    with pytest.raises(HTTPException) as exc_info:
        servicio_consulta.consultar_saldo_y_movimientos("0000000000", "CTA-INEXISTENTE")
        
    assert exc_info.value.status_code == 404
    assert "no coinciden con ningún registro activo" in exc_info.value.detail