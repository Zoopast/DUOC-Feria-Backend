from fastapi import APIRouter, HTTPException, status
from db.client import get_cursor
import cx_Oracle
from db.models.requerimiento import Requerimiento
from db.schemas.requerimiento import requerimiento_tuple_to_dict
from db.schemas.user import user_tuple_to_dict
from db.schemas.producto_requerimiento import producto_tuple_to_dict
router = APIRouter(
    prefix="/requerimientos",
    tags=["requerimientos"],
    responses={404: {"description": "Not found"}},
)

cursor, connection = get_cursor()

async def get_usuario_requerimiento(id_usuario: int):
    cursor.execute("SELECT * FROM USUARIOS WHERE id_usuario = :id_usuario", id_usuario=id_usuario)
    result = cursor.fetchone()
    connection.commit()
    return user_tuple_to_dict(result)

async def get_produtos_requerimiento(id_requerimiento: int):
    cursor.execute("SELECT * FROM PRODUCTO_REQUERIMIENTO WHERE id_requerimiento = :id_requerimiento", id_requerimiento=id_requerimiento)
    result = cursor.fetchall()
    connection.commit()
    return [producto_tuple_to_dict(producto) for producto in result]

@router.get("/")
async def obtener_requerimientos():
    cursor.execute("SELECT * FROM REQUERIMIENTOS")
    result = cursor.fetchall()
    connection.commit()
    return [requerimiento_tuple_to_dict(requerimiento, await get_produtos_requerimiento(requerimiento[0]), await get_usuario_requerimiento(requerimiento[4])) for requerimiento in result]

@router.get("/{id_requerimiento}")
async def obtener_requerimiento(id_requerimiento: int):
    cursor.execute("SELECT * FROM REQUERIMIENTOS WHERE id_requerimiento = :id_requerimiento", id_requerimiento=id_requerimiento)
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Requerimiento no encontrado")
    connection.commit()
    return requerimiento_tuple_to_dict(result, await get_produtos_requerimiento(result[0]), await get_usuario_requerimiento(result[4]))

@router.post("/")
async def crear_requerimiento(requerimiento: Requerimiento):
    nuevo_requerimiento = requerimiento.dict()
    nuevo_requerimiento["estado"] = "enviado"
    del nuevo_requerimiento["id_requerimiento"]
    del nuevo_requerimiento["productos"]

    insert_query = """
        INSERT INTO REQUERIMIENTOS (id_usuario, fecha_inicio, fecha_fin, estado, calidad)
        VALUES (:id_usuario, :fecha_inicio, :fecha_fin, :estado, :calidad)
        RETURNING id_requerimiento INTO :id_requerimiento
    """

    cursor, connection = get_cursor()
    id_requerimiento = cursor.var(cx_Oracle.NUMBER)
    cursor.execute(insert_query, id_requerimiento=id_requerimiento, **nuevo_requerimiento)

    for producto in requerimiento.productos:
        insert_query = """
            INSERT INTO PRODUCTO_REQUERIMIENTO (id_requerimiento, nombre, cantidad)
            VALUES (:id_requerimiento, :nombre, :cantidad)
        """
        producto["id_requerimiento"] = int(id_requerimiento.getvalue()[0])
        cursor.execute(insert_query, producto)

    connection.commit()

    return {"message": "Requerimiento creado exitosamente"}

@router.put("/{id_requerimiento}")
async def actualizar_requerimiento(id_requerimiento: int, requerimiento: Requerimiento):
    nuevo_requerimiento = requerimiento.dict()
    nuevo_requerimiento["id_requerimiento"] = id_requerimiento
    del nuevo_requerimiento["productos"]

    update_query = """
        UPDATE REQUERIMIENTOS
        SET estado = :estado
        WHERE id_requerimiento = :id_requerimiento
    """

    cursor, connection = get_cursor()
    cursor.execute(update_query, id_requerimiento=id_requerimiento, estado=requerimiento.estado)

    connection.commit()

    return {"message": "Requerimiento actualizado exitosamente"}

@router.put("/{id_requerimiento}/estado")
async def actualizar_estado_requerimiento(id_requerimiento: int, requerimiento: Requerimiento):
    nuevo_requerimiento = requerimiento.dict()
    nuevo_requerimiento["id_requerimiento"] = id_requerimiento
    del nuevo_requerimiento["productos"]

    update_query = """
        UPDATE REQUERIMIENTOS
        SET estado = :estado
        WHERE id_requerimiento = :id_requerimiento
    """

    cursor, connection = get_cursor()
    cursor.execute(update_query, id_requerimiento=id_requerimiento, estado=requerimiento.estado)

    connection.commit()

    return {"message": "Estado del requerimiento actualizado exitosamente"}

@router.get("/requisitos_activos")
async def obtener_requisitos_activos():
    cursor.execute("SELECT * FROM REQUERIMIENTOS WHERE estado = 'en curso'")
    result = cursor.fetchall()
    connection.commit()
    return [requerimiento_tuple_to_dict(requerimiento, await get_produtos_requerimiento(requerimiento[0]), await get_usuario_requerimiento(requerimiento[4])) for requerimiento in result]