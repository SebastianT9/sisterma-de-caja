from sqlalchemy.orm import Session
from app.models.credito import Credito
from app.models.amortizacion import TablaAmortizacion
from typing import Optional, List

class CreditoRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear_solicitud(self, id_socio: int, monto: float) -> Credito:
        nueva_solicitud = Credito(id_socio=id_socio, monto_solicitado=monto, estado_credito="Solicitado")
        self.db.add(nueva_solicitud)
        self.db.commit()
        self.db.refresh(nueva_solicitud)
        return nueva_solicitud

    def buscar_credito(self, id_credito: int) -> Optional[Credito]:
        return self.db.query(Credito).filter(Credito.id_credito == id_credito).first()

    def guardar_tabla_amortizacion(self, cuotas: List[TablaAmortizacion]):
        self.db.add_all(cuotas)
        self.db.commit()