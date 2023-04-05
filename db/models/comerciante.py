from pydantic import BaseModel


class Comerciante(BaseModel):
    id_comerciante : str
    nombre: str
    email: str
    telefono: str
    direccion: str