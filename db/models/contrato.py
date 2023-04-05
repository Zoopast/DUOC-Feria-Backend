from pydantic import BaseModel

class Contrato(BaseModel):
    id_contrato: str
    fecha_inicio: str
    fecha_termino: str
    vigente: bool