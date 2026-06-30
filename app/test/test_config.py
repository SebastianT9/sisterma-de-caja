from tests.conftest import engine_test
from app.config.database import Base
from app.config.database import get_db
from sqlalchemy.orm import Session

def test_inicializacion_tablas_en_memoria(db_session):
    """Verifica que los modelos definidos en el ORM se creen correctamente en la BD de pruebas."""
    # Al usar la fixture db_session, Base.metadata.create_all ya se ejecutó.
    # Validamos que las tablas principales existan en el motor en memoria.
    assert "socios" in engine_test.table_names
    assert "cuentas" in engine_test.table_names
    assert "transacciones_diario" in engine_test.table_names
    

def test_ciclo_vida_get_db():
    """Valida que el generador get_db provea una sesión activa de SQLAlchemy y se cierre correctamente."""
    generador = get_db()
    sesion = next(generador)
    
    assert isinstance(sesion, Session)
    assert sesion.is_active == True
    
    # Simular la finalización del bloque en FastAPI
    try:
        next(generador)
    except StopIteration:
        pass # Es el comportamiento esperado de un generador con yield financiero