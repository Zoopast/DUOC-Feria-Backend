from pydantic import BaseModel

class Productor(BaseModel):
    id_productor: int | None
    nombre: str
    email: str
    telefono: str
    direccion: str
    id_contrato: str | None
