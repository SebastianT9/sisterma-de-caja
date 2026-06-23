from fastapi import FastAPI
from app.controllers import socio_controller, transaccion_controller, credito_controller
from app.config.database import Base, engine
import app.models.socio
import app.models.cuenta
import app.models.transaccion
import app.models.credito
import app.models.plan_cuentas
import app.models.amortizacion
app = FastAPI(
    title="Sistema de Cajas de Ahorro",
    description="API Backend automatizada para la gestión financiera, transaccional y contable.",
    version="1.0.0"
)

# Inclusión de los controladores (Routers) que desarrollará el equipo
app.include_router(socio_controller.router, prefix="/api", tags=["Socios & Cuentas"])
app.include_router(transaccion_controller.router, prefix="/api", tags=["Transacciones & Contabilidad"])
app.include_router(credito_controller.router, prefix="/api", tags=["Módulo de Créditos"])

@app.get("/", tags=["Root"])
def read_root():
    return {"status": "Running", "message": "Bienvenidos al Core del Sistema de Cajas de Ahorro"}
# Crea físicamente las tablas mapeadas en la Base de Datos si no existen
Base.metadata.create_all(bind=engine)