from app.services.socio_service import SocioService
from app.services.transaccion_service import TransaccionService
from app.schemas.socio_schemas import SocioCreate
from app.schemas.transaccion_schema import TransaccionCreate
from decimal import Decimal

def test_procesar_deposito_exito(db_session):
    # Crear un socio para tener una cuenta real
    socio_service = SocioService(db_session)
    socio = socio_service.crear_socio_con_cuenta(SocioCreate(cedula="1711111111", nombre="Steven Parra", correo="steven@test.com"))
    num_cuenta = socio.cuentas[0].numero_cuenta

    tx_service = TransaccionService(db_session)
    tx_create = TransaccionCreate(numero_cuenta=num_cuenta, monto=Decimal("150.50"), tipo_movimiento="Deposito")
    
    respuesta = tx_service.procesar_transaccion(tx_create)
    
    assert respuesta["id_transaccion"] is not None
    assert respuesta["tipo_movimiento"] == "Deposito"
    assert respuesta["monto"] == 150.50
    assert respuesta["codigo_cuenta_contable"] == "101.01.01"