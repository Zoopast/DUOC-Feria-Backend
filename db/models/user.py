from pydantic import BaseModel

class Usuario(BaseModel):
    id: int | None
    nombre: str
    email: str

class UsuarioInDB(Usuario):
    password: str | None
    salt: str | None