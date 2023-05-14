from pydantic import BaseModel

class Usuario(BaseModel):
    id_usuario: int | None
    rut: str
    nombre_usuario: str
    apellidos_usuario: str
    email: str
    contrasena: str
    salt: str | None
    rol: str | None
    activo: bool | None

class UsuarioEnSesion(BaseModel):
    id_usuario: int | None
    rut: str
    nombre_usuario: str
    apellidos_usuario: str
    email: str
    rol: str | None
