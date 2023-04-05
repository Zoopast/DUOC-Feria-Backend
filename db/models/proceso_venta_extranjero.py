from pydantic import BaseModel

class ProcesoVentaExtranjero(BaseModel):
    id_proceso_venta: str
    id_contrato: str
    fecha_inicio: str
    fecha_fin: str
    precio_venta: int
    cantidad_producto: str
    