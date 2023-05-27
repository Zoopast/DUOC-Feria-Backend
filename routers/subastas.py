from fastapi import APIRouter, HTTPException, status
from db.client import get_cursor
import cx_Oracle
from db.models.subasta import Subasta
from db.schemas.subasta import subasta_tuple_to_dict
from db.schemas.requerimiento import requerimiento_tuple_to_dict
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

    subasta = subasta_tuple_to_dict(result)
    if not result:
        raise HTTPException(status_code=404, detail="Subasta no encontrado")
    connection.commit()
    
    return subasta

@router.get("/{id_subasta}/info/")
async def obtener_subasta_info(id_subasta: int):
    cursor.execute("SELECT * FROM SUBASTAS WHERE id_subasta = :id_subasta", id_subasta=id_subasta)
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Subasta no encontrado")
    
    subasta = subasta_tuple_to_dict(result)
    cursor.execute("SELECT * FROM REQUERIMIENTOS WHERE id_requerimiento = :id_requerimiento", id_requerimiento=subasta["id_requerimiento"])
    result = cursor.fetchone()
    
    requerimiento = requerimiento_tuple_to_dict(result)
    
    connection.commit()
    return {"subasta": subasta, "requerimiento": requerimiento}

@router.put("/{id_subasta}/finalizar/")
async def finalizar_subasta(id_subasta: int, id_transportista: int):
    update_query = """
        UPDATE SUBASTAS SET estado = 'finalizado', id_transportista = :id_transportista WHERE id_subasta = :id_subasta
    """
    cursor.execute(update_query, id_subasta=id_subasta, id_transportista=id_transportista)
    connection.commit()
    
    get_requerimiento_query = """
        SELECT id_requerimiento FROM SUBASTAS WHERE id_subasta = :id_subasta
    """

    cursor.execute(get_requerimiento_query, id_subasta=id_subasta)
    result = cursor.fetchone()
    id_requerimiento = result[0]

    update_requerimiento_query = """
        UPDATE REQUERIMIENTOS SET estado = 'finalizado' WHERE id_requerimiento = :id_requerimiento"""
    
    cursor.execute(update_requerimiento_query, id_requerimiento=id_requerimiento)

    return {"message": "Subasta finalizada"}