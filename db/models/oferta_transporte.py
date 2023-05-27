from pydantic import BaseModel

class OfertaTransporte(BaseModel):
	id_oferta_transporte: int | None
	id_subasta: int
	id_transportista: int
	precio: int
	fecha_recoleccion: str
	fecha_entrega: str