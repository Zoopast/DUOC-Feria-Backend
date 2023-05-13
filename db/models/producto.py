from pydantic import BaseModel

class Producto(BaseModel):
    id_producto: str | None
    id_productor: str
    nombre: str
    tipo: str
    imagen: str
    calidad: str
    cantidad: str
    precio: int