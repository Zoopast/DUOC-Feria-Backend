from pydantic import BaseModel


class Gasto(BaseModel):
    id_gasto: str
    id_proceso_venta: str
    tipo: str
    monto: str
    fecha: str