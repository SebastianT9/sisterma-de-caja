from sqlalchemy.orm import Session
from app.models.socio import Socio
from app.models.cuenta import Cuenta
from app.schemas.socio_schema import SocioCreate

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