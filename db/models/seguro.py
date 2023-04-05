from pydantic import BaseModel

class Seguro(BaseModel):
    id_seguro: str
    id_transporte_extranjero: str
    cobertura: str
    fecha_inicio: str
    fecha_fin: str
    costo: int