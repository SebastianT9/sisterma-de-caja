from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root_api():
    respuesta = client.get("/")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"status": "Running", "message": "Bienvenidos al Core del Sistema de Cajas de Ahorro"}

def test_http_error_schema_pydantic_socios():
    respuesta = client.post("/api/socios", json={})
    assert respuesta.status_code == 422  

def test_get_consulta_movimientos_parametros_invalidos():
    respuesta = client.get("/api/consulta-movimientos?cedula=12345&numero_cuenta=CTA-01")
    assert respuesta.status_code == 422