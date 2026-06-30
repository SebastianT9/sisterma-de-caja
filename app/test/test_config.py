from tests.conftest import engine_test
from app.config.database import Base

def test_inicializacion_tablas_en_memoria(db_session):
    """Verifica que los modelos definidos en el ORM se creen correctamente en la BD de pruebas."""
    # Al usar la fixture db_session, Base.metadata.create_all ya se ejecutó.
    # Validamos que las tablas principales existan en el motor en memoria.
    assert "socios" in engine_test.table_names
    assert "cuentas" in engine_test.table_names
    assert "transacciones_diario" in engine_test.table_names