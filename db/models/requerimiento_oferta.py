from pydantic import BaseModel

class RequerimientoOferta(BaseModel):
	id_requerimiento_oferta: int | None
	id_requerimiento: int
	id_producto_requerimiento: int
	id_productor: int
	cantidad: int
	precio: int
	aceptado: bool | None


class Ofertas(BaseModel):
	direccion: str
	ofertas: list[RequerimientoOferta]