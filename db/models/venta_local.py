from pydantic import BaseModel

class VentaLocal(BaseModel):
    id_venta_local: str
    id_producto: str
    id_comerciante: str
    cantidad: str
    precio_venta: int
    fecha: str