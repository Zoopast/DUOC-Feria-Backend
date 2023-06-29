from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from db.schemas.venta_local import venta_local_tuple_to_dict_schema
from db.client import get_cursor
from datetime import datetime, timedelta
from utils.usuarios import get_current_user
cursor, connection = get_cursor()
router = APIRouter(
    prefix="/ventas-locales",
    tags=["ventas_locales"],
    # dependencies=[Depends(get_token_header)],
		responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_ventas_locales():
		query = """
			SELECT VL.*, RO.*, PR.nombre, PR.calidad, P.nombre_usuario, P.apellidos_usuario
			FROM VENTAS_LOCALES VL
			INNER JOIN REQUERIMIENTO_OFERTA RO ON VL.id_producto_rechazado = RO.id_requerimiento_oferta
			INNER JOIN PRODUCTO_REQUERIMIENTO PR ON RO.id_producto_requerimiento = PR.id_producto_requerimiento
			INNER JOIN USUARIOS P ON RO.id_productor = P.id_usuario
		"""
		cursor.execute(query)
		result = cursor.fetchall()
		connection.commit()
		return [venta_local_tuple_to_dict_schema(venta_local) for venta_local in result]

@router.post("/")
async def crear_venta_local(id_productos_rechazados: List[int]):
		for id_producto_rechazado in id_productos_rechazados:
				new_venta_local_query = """
				INSERT INTO VENTAS_LOCALES (id_producto_rechazado, fecha_inicio, fecha_fin)
				VALUES (:id_producto_rechazado, :fecha_inicio, :fecha_fin)
				"""
				cursor.execute(new_venta_local_query,
		   								 id_producto_rechazado=id_producto_rechazado,
											 fecha_inicio=datetime.now().strftime("%d-%b-%Y"),
											 fecha_fin=(datetime.now() + timedelta(days=3)).strftime("%d-%b-%Y"))

		connection.commit()
		return {"message": "Venta local creada exitosamente"}

@router.get("/{id_venta_local}")
async def get_venta_local(id_venta_local: int):

		query = """
			SELECT VL.*, RO.*, PR.nombre, PR.calidad, P.nombre_usuario, P.apellidos_usuario
			FROM VENTAS_LOCALES VL
			INNER JOIN REQUERIMIENTO_OFERTA RO ON VL.id_producto_rechazado = RO.id_requerimiento_oferta
			INNER JOIN PRODUCTO_REQUERIMIENTO PR ON RO.id_producto_requerimiento = PR.id_producto_requerimiento
			INNER JOIN USUARIOS P ON RO.id_productor = P.id_usuario
			WHERE id_venta_local = :id_venta_local
		"""

		cursor.execute(query, id_venta_local=id_venta_local)
		result = cursor.fetchone()
		if not result:
				raise HTTPException(status_code=404, detail="Venta local no encontrada")
		connection.commit()
		return venta_local_tuple_to_dict_schema(result)

@router.get("/activos/")
async def get_ventas_locales_activas():
		get_ventas_locales_activas_query = """
		SELECT VL.*, RO.*, PR.nombre, PR.calidad, P.nombre_usuario, P.apellidos_usuario
		FROM VENTAS_LOCALES VL
		INNER JOIN REQUERIMIENTO_OFERTA RO ON VL.id_producto_rechazado = RO.id_requerimiento_oferta
		INNER JOIN PRODUCTO_REQUERIMIENTO PR ON RO.id_producto_requerimiento = PR.id_producto_requerimiento
		INNER JOIN USUARIOS P ON RO.id_productor = P.id_usuario
		WHERE VL.estado = 'activo' AND VL.fecha_fin >= :fecha_actual
		"""
		cursor.execute(get_ventas_locales_activas_query, fecha_actual=datetime.now().strftime("%d-%b-%Y"))
		result = cursor.fetchall()
		connection.commit()
		return [venta_local_tuple_to_dict_schema(venta_local) for venta_local in result]

@router.post('/finalize-past-sales')
async def finalize_past_sales():
		get_past_sales_query = """
		SELECT * FROM VENTAS_LOCALES WHERE fecha_fin < :fecha_actual
		"""
		cursor.execute(get_past_sales_query, fecha_actual=datetime.now().strftime("%d-%b-%Y"))
		result = cursor.fetchall()
		for venta_local in result:
				finalize_past_sale_query = """
				UPDATE VENTAS_LOCALES SET estado = 'finalizado' WHERE id_venta_local = :id_venta_local
				"""
				cursor.execute(finalize_past_sale_query, id_venta_local=venta_local[0])
		connection.commit()
		return {"message": "Ventas locales finalizadas"}

@router.post('/{id_venta_local}/comprar/')
async def comprar_venta_local(id_venta_local: int, user=Depends(get_current_user)):
	try:
		comprar_venta_local_query = """
		UPDATE VENTAS_LOCALES SET estado = 'comprado', id_comprador=:id_usuario
		WHERE id_venta_local = :id_venta_local
		"""
		cursor.execute(comprar_venta_local_query, id_venta_local=id_venta_local, id_usuario=user.id_usuario)
		connection.commit()
	except Exception as e:
		print(e)
		raise HTTPException(status_code=400, detail="Error comprando venta local")

	return {"message": "Venta local comprada"}

@router.post('/finalize-sale/{id_venta_local}')
async def finalize_sale(id_venta_local: int):
		try:
			finalize_sale_query = """
			UPDATE VENTAS_LOCALES SET estado = 'finalizado' WHERE id_venta_local = :id_venta_local
			"""
			cursor.execute(finalize_sale_query, id_venta_local=id_venta_local)
			connection.commit()
		except Exception as e:
			raise HTTPException(status_code=404, detail="Venta local no encontrada")

		return {"message": "Venta local finalizada"}