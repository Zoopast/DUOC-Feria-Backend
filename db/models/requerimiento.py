from pydantic import BaseModel

class Requerimiento(BaseModel):

    id_requerimiento: int | None
    id_usuario: int
    fecha_inicio: str
    fecha_fin: str
    estado: str | None = "enviado"
    calidad: str
    productos: list[object] | None

    def check_estado(self):
        estados = ["enviado", "activo", "rechazado", "en proceso", "finalizado"]
        if self.estado not in estados:
            raise ValueError("Estado inválido")