from pydantic import BaseModel

class Pago(BaseModel):
    id_pago: str
    id_proceso_venta: str
    id_venta_local: str
    id_productor: str
    monto: str
    fecha: str