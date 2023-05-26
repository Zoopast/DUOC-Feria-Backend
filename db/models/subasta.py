from pydantic import BaseModel

class Subasta(BaseModel):
	id_subasta: int | None
	id_usuario: int
	fecha_inicio: str
	fecha_fin: str
	estado: str | None = "enviado"
	id_transportista: int | None

	