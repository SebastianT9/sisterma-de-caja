from sqlalchemy.orm import Session
from app.models.socio import Socio
from app.models.cuenta import Cuenta
from app.schemas.socio_schemas import SocioCreate
from app.models.transaccion import TransaccionDiario
from typing import Optional, List

class SocioRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_por_cedula(self, cedula: str) -> Optional[Socio]:
        return self.db.query(Socio).filter(Socio.cedula == cedula).first()

    def registrar_socio(self, socio_data: SocioCreate) -> Socio:
        nuevo_socio = Socio(
            cedula=socio_data.cedula,
            nombre=socio_data.nombre,
            correo=socio_data.correo
        )
        self.db.add(nuevo_socio)
        self.db.commit()
        self.db.refresh(nuevo_socio)
        return nuevo_socio

    def vincular_cuenta(self, id_socio: int, numero_cuenta: str, tipo_cuenta: str) -> Cuenta:
        nueva_cuenta = Cuenta(
            id_socio=id_socio,
            numero_cuenta=numero_cuenta,
            tipo_cuenta=tipo_cuenta,
            saldo_actual=0.00
        )
        self.db.add(nueva_cuenta)
        self.db.commit()
        self.db.refresh(nueva_cuenta)
        return nueva_cuenta
    
class ConsultaRepository:
    def _init_(self, db: Session):
        self.db = db

    def verificar_socio_y_cuenta(self, cedula: str, numero_cuenta: str) -> Optional[Cuenta]:
        # Busca la cuenta y valida que pertenezca al socio con la cédula provista
        return self.db.query(Cuenta).join(Socio).filter(
            Socio.cedula == cedula,
            Cuenta.numero_cuenta == numero_cuenta
        ).first()

    def obtener_ultimos_tres_movimientos(self, id_cuenta: int) -> List[TransaccionDiario]:
        # Corresponde al diseño exacto: SELECT TOP 3 ... ORDER BY fecha DESC
        return self.db.query(TransaccionDiario).filter(
            TransaccionDiario.id_cuenta == id_cuenta
        ).order_by(TransaccionDiario.fecha_transaccion.desc()).limit(3).all()