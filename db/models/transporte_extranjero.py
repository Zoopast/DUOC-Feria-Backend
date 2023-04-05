from pydantic import BaseModel

class TransporteExtranjero(BaseModel):
    id_transporte_extranjero: str
    id_proceso_venta: str
    nombre_transportista: str
    fecha_salida: str
    fecha_llegada: str
    costo: int