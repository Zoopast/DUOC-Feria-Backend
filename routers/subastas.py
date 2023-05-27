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

@router.post("/")
async def crear_subasta(subasta: Subasta):
    nuevo_subasta = subasta.dict()
    nuevo_subasta["estado"] = "enviado"
    nuevo_subasta["fecha_inicio"] = datetime.strptime(nuevo_subasta["fecha_inicio"], "%d/%m/%Y").strftime("%d-%b-%Y")
    nuevo_subasta["fecha_fin"] = datetime.strptime(nuevo_subasta["fecha_fin"], "%d/%m/%Y").strftime("%d-%b-%Y")
    
    del nuevo_subasta["id_subasta"]
    del nuevo_subasta["productos"]


    insert_query = """
        INSERT INTO SUBASTAS (id_usuario, fecha_inicio, fecha_fin, estado, calidad)
        VALUES (:id_usuario, :fecha_inicio, :fecha_fin, :estado, :calidad)
        RETURNING id_subasta INTO :id_subasta
    """

    cursor, connection = get_cursor()
    id_subasta = cursor.var(cx_Oracle.NUMBER)
    cursor.execute(insert_query, id_subasta=id_subasta, **nuevo_subasta)

    for producto in subasta.productos:
        insert_query = """
            INSERT INTO PRODUCTO_SUBASTA (id_subasta, nombre, cantidad)
            VALUES (:id_subasta, :nombre, :cantidad)
        """
        producto["id_subasta"] = int(id_subasta.getvalue()[0])
        cursor.execute(insert_query, producto)

    connection.commit()

    return {"message": "Subasta creado exitosamente"}

@router.put("/{id_subasta}")
async def actualizar_subasta(id_subasta: int, subasta: Subasta):
    nuevo_subasta = subasta.dict()
    nuevo_subasta["id_subasta"] = id_subasta
    del nuevo_subasta["productos"]

    update_query = """
        UPDATE SUBASTAS
        SET estado = :estado
        WHERE id_subasta = :id_subasta
    """

    cursor, connection = get_cursor()
    cursor.execute(update_query, id_subasta=id_subasta, estado=subasta.estado)

    connection.commit()

    return {"message": "Subasta actualizado exitosamente"}

@router.put("/{id_subasta}/estado")
async def actualizar_estado_subasta(id_subasta: int, subasta: Subasta):
    nuevo_subasta = subasta.dict()
    nuevo_subasta["id_subasta"] = id_subasta
    del nuevo_subasta["productos"]

    update_query = """
        UPDATE SUBASTAS
        SET estado = :estado
        WHERE id_subasta = :id_subasta
    """

    cursor, connection = get_cursor()
    cursor.execute(update_query, id_subasta=id_subasta, estado=subasta.estado)

    connection.commit()

    return {"message": "Estado del subasta actualizado exitosamente"}

@router.get("/requisitos_activos")
async def obtener_requisitos_activos():
    cursor.execute("SELECT * FROM SUBASTAS WHERE estado = 'activo'")
    result = cursor.fetchall()
    connection.commit()
    return [subasta_tuple_to_dict(subasta) for subasta in result]