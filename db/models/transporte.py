from pydantic import BaseModel

class Transporte(BaseModel):
    id_transporte: str
    id_productor: str
    id_comerciante: str
    fecha_recoleccion: str
    fecha_entrega: str
    costo: int