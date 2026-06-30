from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root_api():
    respuesta = client.get("/")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"status": "Running", "message": "Bienvenidos al Core del Sistema de Cajas de Ahorro"}

def test_http_error_schema_pydantic_socios():
    # Enviar un JSON vacío a la ruta de creación para forzar el fallo de validación de esquemas de Pydantic
    respuesta = client.post("/api/socios", json={})
    assert respuesta.status_code == 422  # Unprocessable Entity (Error nativo de validación de FastAPI)