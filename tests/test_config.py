from tests.conftest import engine_test
from app.config.database import Base, get_db  # <-- IMPORTANTE: Se añade get_db
from sqlalchemy import inspect
from sqlalchemy.orm import Session  # <-- IMPORTANTE: Se añade Session

# Forzar el registro unificado de todos los modelos en la metadata de SQLAlchemy
import app.models.socio
import app.models.cuenta
import app.models.transaccion
import app.models.credito
import app.models.plan_cuentas
import app.models.amortizacion

def test_inicializacion_tablas_en_memoria(db_session):
    """Verifica que los modelos definidos en el ORM se creen correctamente en la BD de pruebas."""
    Base.metadata.create_all(bind=engine_test)
    
    inspector = inspect(engine_test)
    tablas = inspector.get_table_names()
    
    assert "socios" in tablas
    assert "cuentas" in tablas
    assert "transacciones_diario" in tablas

def test_ciclo_vida_get_db():
    """Valida que el generador get_db provea una sesión activa de SQLAlchemy y se cierre correctamente."""
    generador = get_db()
    sesion = next(generador)
    
    assert isinstance(sesion, Session)
    assert sesion.is_active == True
    
    try:
        next(generador)
    except StopIteration:
        pass  