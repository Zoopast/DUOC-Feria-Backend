from pydantic import BaseModel

class Usuario(BaseModel):
    id: int
    nombre: str
    rol_id: int

