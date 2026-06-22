# Sistema de Cajas de Ahorro - Grupo 3

## Integrantes
* Bastidas Arias Roberth Jossue
* Campuez De La Cruz Mayerli Julieth
* Izquierdo Oñate Fabian Liam
* Parra León Steven Alexis
* Tipantuña Toaquiza Jonathan Sebastián

## 1. Requerimientos Base (SRS)
* **REQ-F-02 [Socios]:** Registro e información de cuentas.
* **REQ-F-03 [Aportaciones/Ahorros]:** Transacciones (Depósitos/Retiros).
* **REQ-F-04 [Servicio Web]:** Consulta remota (Últimos 3 movimientos y saldo).
* **REQ-F-05 [Créditos]:** Ciclo de vida y tablas de amortización.
* **REQ-F-06 [Contabilidad]:** Envío automático al Libro Diario.

## 2. Diseño Arquitectónico (DDS)
Este sistema implementa una arquitectura limpia por capas:
* **Capa de Controladores:** API REST expuesta y documentada.
* **Capa de Servicios:** Lógica de negocio y reglas financieras.
* **Capa de Dominio/Modelos:** Entidades del core bancario.
* **Capa de Persistencia:** Acceso a Base de Datos relacional.

## 3. Instalación de Requirementes (Se debe correr el siguiente comando en consola para iniciar el programa)

* **Instalar requerimientos:** python -m pip install -r requirements.txt
* **Correr el código:** python -m uvicorn app.main:app --reload
* **Correr el código:** Abrir el enlace de con la siguiente ruta de manera local http://127.0.0.1:8000/docs