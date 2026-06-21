from sqlalchemy.orm import Session
from app.models.cuenta import Cuenta
from app.models.transaccion import TransaccionDiario
from decimal import Decimal
from typing import Optional

class TransaccionRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_cuenta_por_numero(self, numero_cuenta: str) -> Optional[Cuenta]:
        return self.db.query(Cuenta).filter(Cuenta.numero_cuenta == numero_cuenta).first()

    def actualizar_saldo_cuenta(self, cuenta: Cuenta, nuevo_saldo: Decimal):
        cuenta.saldo_actual = nuevo_saldo
        self.db.add(cuenta)

    def registrar_asiento_diario(self, id_cuenta: int, codigo_contable: str, tipo: str, monto: Decimal) -> TransaccionDiario:
        nuevo_asiento = TransaccionDiario(
            id_cuenta=id_cuenta,
            codigo_cuenta_contable=codigo_contable,
            tipo_movimiento=tipo,
            monto=monto
        )
        self.db.add(nuevo_asiento)
        return nuevo_asiento    