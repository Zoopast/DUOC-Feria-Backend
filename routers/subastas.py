from fastapi import APIRouter, HTTPException, status
from db.client import get_cursor
import cx_Oracle
from db.models.subasta import Subasta
from db.schemas.subasta import subasta_tuple_to_dict
from datetime import datetime

router = APIRouter(
    prefix="/subastas",
    tags=["subastas"],
    responses={404: {"description": "Not found"}},
)

cursor, connection = get_cursor()

@router.get("/activas")
async def obtener_subastas_activas():
    cursor.execute("SELECT * FROM SUBASTAS WHERE estado = 'activo'")
    result = cursor.fetchall()
    connection.commit()
    return [subasta_tuple_to_dict(subasta) for subasta in result]

@router.get("/")
async def obtener_subastas():
    cursor.execute("SELECT * FROM SUBASTAS")
    result = cursor.fetchall()
    connection.commit()
    return [subasta_tuple_to_dict(subasta) for subasta in result]

@router.get("/{id_subasta}")
async def obtener_subasta(id_subasta: int):
    cursor.execute("SELECT * FROM SUBASTAS WHERE id_subasta = :id_subasta", id_subasta=id_subasta)
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Subasta no encontrado")
    connection.commit()
    return subasta_tuple_to_dict(result)

@router.put("/{id_subasta}/finalizar/")
async def finalizar_subasta(id_subasta: int, id_transportista: int):
    update_query = """
        UPDATE SUBASTAS SET estado = 'finalizado', id_transportista = :id_transportista WHERE id_subasta = :id_subasta
    """

    cursor.execute(update_query, id_subasta=id_subasta, id_transportista=id_transportista)
    connection.commit()
    return {"message": "Subasta finalizada"}