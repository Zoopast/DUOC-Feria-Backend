from pydantic import BaseModel

class Subasta(BaseModel):
	id_subasta: int | None
	id_requerimiento: int
	fecha_inicio: str
	fecha_fin: str
	estado: str | None = "activo"
	id_transportista: int | None

	