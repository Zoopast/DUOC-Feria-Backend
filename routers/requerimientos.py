from fastapi import APIRouter, HTTPException, status
from db.client import get_cursor
import cx_Oracle
from typing import List
from db.models.requerimiento import Requerimiento
from db.models.requerimiento_oferta import Ofertas
from db.schemas.requerimiento import requerimiento_tuple_to_dict, requerimiento_oferta_tuple_to_dict
from db.schemas.user import user_tuple_to_dict
from db.schemas.producto_requerimiento import producto_tuple_to_dict
from datetime import datetime, timedelta

cursor, connection = get_cursor()

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
    return [requerimiento_tuple_to_dict(requerimiento, await get_produtos_requerimiento(requerimiento[0]), await get_usuario_requerimiento(requerimiento[3])) for requerimiento in result]

@router.get("/{id_requerimiento}")
async def obtener_requerimiento(id_requerimiento: int):
    cursor.execute("SELECT * FROM REQUERIMIENTOS WHERE id_requerimiento = :id_requerimiento", id_requerimiento=id_requerimiento)
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Requerimiento no encontrado")
    connection.commit()
    return requerimiento_tuple_to_dict(result, await get_produtos_requerimiento(result[0]), await get_usuario_requerimiento(result[3]))

@router.get("/{id_requerimiento}/ofertas/")
async def obtener_requerimiento(id_requerimiento: int):
    try:
        cursor.execute("SELECT * FROM REQUERIMIENTOS WHERE id_requerimiento = :id_requerimiento", id_requerimiento=id_requerimiento)
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Requerimiento no encontrado")

        ofertas_query = """
            SELECT RO.*, U.nombre_usuario, U.apellidos_usuario
            FROM REQUERIMIENTO_OFERTA RO
            JOIN USUARIOS U ON RO.id_productor = U.id_usuario
            WHERE RO.id_requerimiento = :id_requerimiento
        """

        cursor.execute(ofertas_query, id_requerimiento=id_requerimiento)
        result = cursor.fetchall()
        if not result:
            return []
        connection.commit()
        return [requerimiento_oferta_tuple_to_dict(oferta) for oferta in result]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error al obtener ofertas")

@router.post("/")
async def crear_requerimiento(requerimiento: Requerimiento):
    nuevo_requerimiento = requerimiento.dict()
    nuevo_requerimiento["estado"] = "enviado"
    nuevo_requerimiento["fecha_inicio"] = datetime.strptime(nuevo_requerimiento["fecha_inicio"],
                                                            "%d/%m/%Y").strftime("%d-%b-%Y")
    nuevo_requerimiento["fecha_fin"] = datetime.strptime(nuevo_requerimiento["fecha_fin"],
                                                         "%d/%m/%Y").strftime("%d-%b-%Y")

    del nuevo_requerimiento["id_requerimiento"]
    del nuevo_requerimiento["productos"]


    insert_query = """
        INSERT INTO REQUERIMIENTOS (id_usuario, fecha_inicio, fecha_fin, estado, direccion)
        VALUES (:id_usuario, :fecha_inicio, :fecha_fin, :estado, :direccion)
        RETURNING id_requerimiento INTO :id_requerimiento
    """

    cursor, connection = get_cursor()
    id_requerimiento = cursor.var(cx_Oracle.NUMBER)
    cursor.execute(insert_query, id_requerimiento=id_requerimiento, **nuevo_requerimiento)

    for producto in requerimiento.productos:
        insert_query = """
            INSERT INTO PRODUCTO_REQUERIMIENTO (id_requerimiento, nombre, cantidad, calidad)
            VALUES (:id_requerimiento, :nombre, :cantidad, :calidad)
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

async def create_contrato(id_requerimiento: int, id_cliente: int):
    try:
        query = """
            INSERT INTO CONTRATOS (id_requerimiento, id_cliente)
            VALUES (:id_requerimiento, :id_cliente)
        """
        cursor.execute(query, id_requerimiento=id_requerimiento, id_cliente=id_cliente)
    except:
        raise HTTPException(status_code=500, detail="Error al crear contrato")

@router.put("/{id_requerimiento}/estado")
async def actualizar_estado_requerimiento(id_requerimiento: int, requerimiento: Requerimiento):
    try:
        nuevo_requerimiento = requerimiento.dict()
        nuevo_requerimiento["id_requerimiento"] = id_requerimiento
        del nuevo_requerimiento["productos"]

        update_query = """
            UPDATE REQUERIMIENTOS
            SET estado = :estado
            WHERE id_requerimiento = :id_requerimiento
        """

        cursor.execute(update_query, id_requerimiento=id_requerimiento, estado=requerimiento.estado)

        if requerimiento.estado == "activo":
            await create_contrato(id_requerimiento, requerimiento.id_usuario)
        
        connection.commit()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error al actualizar estado del requerimiento")

    if requerimiento.estado == "activo":
        await create_contrato(id_requerimiento, requerimiento.id_usuario)
    return {"message": "Estado del requerimiento actualizado exitosamente"}

@router.get("/activos/")
async def obtener_requerimientos_activos():
    cursor.execute("SELECT * FROM REQUERIMIENTOS WHERE estado = 'activo'")
    result = cursor.fetchall()
    connection.commit()
    return [requerimiento_tuple_to_dict(requerimiento, await get_produtos_requerimiento(requerimiento[0]), await get_usuario_requerimiento(requerimiento[3])) for requerimiento in result]

@router.post("/productos/oferta/")
async def hacer_oferta(ofertas: Ofertas):
    direccion = ofertas.direccion

    try:
        for oferta in ofertas.ofertas:
            nueva_oferta = oferta.dict()
            del nueva_oferta["id_requerimiento_oferta"]
            del nueva_oferta["aceptado"]
            nueva_oferta["precio"] = int(nueva_oferta["precio"])
            nueva_oferta["direccion"] = direccion
            insert_query = """
                INSERT INTO REQUERIMIENTO_OFERTA
                (id_requerimiento, id_producto_requerimiento, id_productor, cantidad, precio, direccion)
                VALUES (:id_requerimiento, :id_producto_requerimiento, :id_productor, :cantidad, :precio, :direccion)
            """

            cursor, connection = get_cursor()
            cursor.execute(insert_query, **nueva_oferta)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="No se pudo realizar la oferta")

    connection.commit()
    return {"message": "Oferta realizada exitosamente"}

async def create_productor_cliente_contrato(id_cliente, id_productor, id_contrato, id_oferta):
    try:
        query = """
            INSERT INTO PRODUCTOR_CLIENTE_CONTRATOS (id_cliente, id_productor, id_contrato, id_oferta)
            VALUES (:id_cliente, :id_productor, :id_contrato, :id_oferta)
        """
        cursor.execute(query, id_cliente=id_cliente, id_productor=id_productor, id_contrato=id_contrato, id_oferta=id_oferta)
    except:
        raise HTTPException(status_code=500, detail="Error al crear contrato")

@router.put("/{id_requerimiento}/ofertas/aceptar/")
async def aceptar_oferta(id_requerimiento: int, ofertas: List[int]):

    for id_oferta in ofertas:
        update_query = """
        UPDATE REQUERIMIENTO_OFERTA SET aceptado = 1 WHERE id_requerimiento_oferta = :id_requerimiento_oferta
        """
        cursor.execute(update_query, id_requerimiento_oferta=id_oferta)

        find_contrato_query = """
            SELECT RO.id_productor, C.id_contrato, C.id_cliente FROM CONTRATOS 
            INNER JOIN REQUERIMIENTO_OFERTA RO ON RO.id_requerimiento = CONTRATOS.id_requerimiento
            WHERE id_requerimiento = :id_requerimiento
        """

        cursor.execute(find_contrato_query, id_requerimiento=id_requerimiento)
        
        id_productor = cursor.fetchone()[0]
        id_contrato = cursor.fetchone()[0]
        id_cliente = cursor.fetchone()[1]
        
        await create_productor_cliente_contrato(id_cliente, id_productor, id_contrato, id_oferta)
        



    connection.commit()

    nueva_subasta_query = """
        INSERT INTO SUBASTAS (id_requerimiento, fecha_inicio, fecha_fin, estado) VALUES
        (:id_requerimiento, :fecha_inicio, :fecha_fin, :estado)
    """

    cursor.execute(nueva_subasta_query,
                   id_requerimiento=id_requerimiento,
                   fecha_inicio = datetime.now().strftime("%d-%b-%Y"),
                   fecha_fin = (datetime.now() + timedelta(days=7)).strftime("%d-%b-%Y"),
                   estado="activo")

    return {"message": "Ofertas aceptada exitosamente"}

@router.put("/{id_requerimiento}/finalizar/")
async def finalizar_requerimiento(id_requerimiento: int):
    update_query = """
        UPDATE REQUERIMIENTOS SET estado = 'finalizado' WHERE id_requerimiento = :id_requerimiento
    """

    cursor.execute(update_query, id_requerimiento=id_requerimiento)

    update_subasta_query = """
        UPDATE SUBASTAS SET estado = 'finalizado' WHERE id_requerimiento = :id_requerimiento
    """

    cursor.execute(update_subasta_query, id_requerimiento=id_requerimiento)

    connection.commit()

    return {"message": "Requerimiento finalizado exitosamente"}

@router.delete("/")
async def eliminar_requerimiento(id_requerimiento: int):
    delete_query = """
        DELETE FROM REQUERIMIENTOS WHERE id_requerimiento = :id_requerimiento
    """

    cursor.execute(delete_query, id_requerimiento=id_requerimiento)

    connection.commit()

    return {"message": "Requerimiento eliminado exitosamente"}

@router.delete("/all/")
async def eliminar_requerimientos():
    delete_query = """
        DELETE FROM REQUERIMIENTOS
    """

    cursor.execute(delete_query)

    connection.commit()

    return {"message": "Requerimientos eliminados exitosamente"}