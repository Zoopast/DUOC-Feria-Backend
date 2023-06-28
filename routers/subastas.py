from fastapi import APIRouter, HTTPException, status
from db.client import get_cursor
import cx_Oracle
from db.models.subasta import Subasta
from db.schemas.subasta import subasta_tuple_to_dict
from db.schemas.requerimiento import requerimiento_tuple_to_dict
from datetime import datetime
from db.schemas.producto_requerimiento import producto_tuple_to_dict, producto_subasta_tuple_to_dict
from db.schemas.oferta_transporte import oferta_tuple_to_dict
from db.models.oferta_transporte import OfertaTransporte
router = APIRouter(
    prefix="/subastas",
    tags=["subastas"],
    responses={404: {"description": "Not found"}},
)

cursor, connection = get_cursor()

def set_direccion(direccion):
    return {
        "id_producto_requerimiento": direccion[0],
        "direccion": direccion[1]
    }

async def get_direcciones_productos_requerimiento(id_requerimiento: int):
    query = """
        SELECT id_producto_requerimiento, direccion FROM REQUERIMIENTO_OFERTA
        WHERE id_requerimiento = :id_requerimiento AND ACEPTADO = 1
    """

    cursor.execute(query, id_requerimiento=id_requerimiento)
    result = cursor.fetchall()

    connection.commit()

    return [set_direccion(direccion) for direccion in result]


async def get_produtos_requerimiento(id_requerimiento: int):
    cursor.execute("SELECT * FROM PRODUCTO_REQUERIMIENTO WHERE id_requerimiento = :id_requerimiento", id_requerimiento=id_requerimiento)
    result = cursor.fetchall()
    connection.commit()
    return [producto_tuple_to_dict(producto) for producto in result]

async def get_ofertas_transporte(id_subasta: int):
    ofertas_query = """
    SELECT OT.*, U.nombre_usuario, U.apellidos_usuario
    FROM OFERTA_TRANSPORTE OT
    JOIN USUARIOS U ON OT.id_transportista = U.id_usuario
    WHERE OT.id_subasta = :id_subasta
    """
    cursor.execute(ofertas_query, id_subasta=id_subasta)
    result = cursor.fetchall()
    connection.commit()
    return [oferta_tuple_to_dict(oferta) for oferta in result]

@router.get("/activas/")
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

    subasta_query = """
    SELECT * FROM SUBASTAS
    WHERE id_subasta = :id_subasta
    """

    cursor.execute(subasta_query, id_subasta=id_subasta)
    subasta = cursor.fetchone()

    if subasta[5]:
        find_user_query = """
            SELECT nombre_usuario, apellidos_usuario FROM USUARIOS WHERE id_usuario = :id_usuario
        """
        cursor.execute(find_user_query, id_usuario=subasta[5])
        user = cursor.fetchone()
        subasta = {
            "id_subasta" : subasta[0],
            "id_requerimiento" : subasta[1],
            "fecha_inicio" : subasta[2],
            "fecha_fin" : subasta[3],
            "estado": subasta[4],
            "transportista": {"id_transportista": subasta[5],  "nombre": user[0] + " " + user[1] }
        }
    else:
        subasta = {
            "id_subasta" : subasta[0],
            "id_requerimiento" : subasta[1],
            "fecha_inicio" : subasta[2],
            "fecha_fin" : subasta[3],
            "estado": subasta[4],
            "transportista": None
        }

    requerimiento_query = """
        SELECT REQUERIMIENTOS.*, USUARIOS.nombre_usuario, USUARIOS.apellidos_usuario
        FROM REQUERIMIENTOS
        JOIN USUARIOS ON REQUERIMIENTOS.id_usuario = USUARIOS.id_usuario
        WHERE REQUERIMIENTOS.id_requerimiento = :id_requerimiento
    """
    cursor.execute(requerimiento_query, id_requerimiento=subasta["id_requerimiento"])

    requerimiento_info = cursor.fetchone()
    productos = await get_produtos_requerimiento(subasta["id_requerimiento"])
    ofertas = await get_ofertas_transporte(id_subasta)
    direcciones_productos = await get_direcciones_productos_requerimiento(subasta["id_requerimiento"])

    print(direcciones_productos)

    for producto in productos:
        producto["direcciones"] = []
        for direccion_producto in direcciones_productos:
            print(direccion_producto["id_producto_requerimiento"])
            if producto["id_producto"] == direccion_producto["id_producto_requerimiento"]:
                producto["direcciones"].append(direccion_producto["direccion"])
                break
    

    connection.commit()

    requerimiento = {
        "id_requerimiento": requerimiento_info[0],
        "fecha_inicio": requerimiento_info[1],
        "fecha_fin": requerimiento_info[2],
        "estado": requerimiento_info[4],
        "direccion": requerimiento_info[5],
        "usuario": {
            "id_usuario": requerimiento_info[3],
            "nombre": requerimiento_info[6] + " " + requerimiento_info[7]
        },
        "productos": productos
    }

    print(requerimiento, subasta, ofertas)

    return {
        "subasta": subasta,
        "requerimiento": requerimiento,
        "ofertas": ofertas
    }

@router.put("/{id_subasta}/finalizar/")
async def finalizar_subasta(id_subasta: int, id_transportista: int):
    update_query = """
        UPDATE SUBASTAS SET estado = 'en preparación', id_transportista = :id_transportista WHERE id_subasta = :id_subasta
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
        UPDATE REQUERIMIENTOS SET estado = 'en preparación' WHERE id_requerimiento = :id_requerimiento"""

    cursor.execute(update_requerimiento_query, id_requerimiento=id_requerimiento)

    return {"message": "Subasta finalizada"}

@router.get("/won/")
async def obtener_subastas_ganadas(id_transportista: int):
    cursor.execute("SELECT * FROM SUBASTAS WHERE id_transportista = :id_transportista", id_transportista=id_transportista)
    result = cursor.fetchall()
    connection.commit()
    return [subasta_tuple_to_dict(subasta) for subasta in result]

@router.post("/actualizar/envio/recogido/")
async def actualizar_envio_recogido(id_subasta: int, id_requerimiento: int):
    update_query = """
        UPDATE SUBASTAS SET estado = 'en camino' WHERE id_subasta = :id_subasta
    """
    cursor.execute(update_query, id_subasta=id_subasta)

    update_requerimiento_query = """
        UPDATE REQUERIMIENTOS SET estado = 'en camino' WHERE id_requerimiento = :id_requerimiento
    """

    cursor.execute(update_requerimiento_query, id_requerimiento=id_requerimiento)

    connection.commit()
    return {"message": "Envío recogido"}

@router.post("/actualizar/envio/entregado/")
async def actualizar_envio_entregado(id_subasta: int, id_requerimiento: int):
    update_query = """
        UPDATE SUBASTAS SET estado = 'entregado' WHERE id_subasta = :id_subasta
    """
    cursor.execute(update_query, id_subasta=id_subasta)

    update_requerimiento_query = """
        UPDATE REQUERIMIENTOS SET estado = 'entregado' WHERE id_requerimiento = :id_requerimiento
    """

    cursor.execute(update_requerimiento_query, id_requerimiento=id_requerimiento)

    connection.commit()
    return {"message": "Envío entregado"}


@router.post("/ofertas/hacer_oferta/")
async def hacer_oferta(oferta_transporte: OfertaTransporte):
    oferta_dict = oferta_transporte.dict()
    oferta_dict["fecha_recoleccion"] = datetime.strptime(oferta_dict["fecha_recoleccion"], "%d/%m/%Y").strftime("%d-%b-%Y")
    oferta_dict["fecha_entrega"] = datetime.strptime(oferta_dict["fecha_entrega"], "%d/%m/%Y").strftime("%d-%b-%Y")

    del oferta_dict["id_oferta_transporte"]
    insert_query = """
        INSERT INTO OFERTA_TRANSPORTE (id_subasta, id_transportista, precio, fecha_recoleccion, fecha_entrega)
        VALUES (:id_subasta, :id_transportista, :precio, :fecha_recoleccion, :fecha_entrega)
    """
    cursor.execute(insert_query,
                   oferta_dict)
    connection.commit()
    return {"message": "Oferta realizada"}