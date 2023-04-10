from pydantic import BaseModel
class Comerciante(BaseModel):
    id_comerciante: int | None
    nombre: str
    email: str
    telefono: str
    direccion: str
    id_usuario: str | None