def venta_local_tuple_to_dict_schema(venta_local: tuple) -> list:
    return {
        "id_venta_local": venta_local[0],
        "id_producto_rechazado": venta_local[1],
        "fecha_inicio": venta_local[2],
        "fecha_fin": venta_local[3],
        "estado": venta_local[4],
        "id_requerimiento_oferta": venta_local[5],
        "id_requerimiento": venta_local[6],
        "id_producto_requerimiento": venta_local[7],
        "id_productor": venta_local[8],
        "cantidad": venta_local[9],
        "precio": venta_local[10],
        "aceptado": venta_local[11],
        "nombre": venta_local[12],
        "calidad": venta_local[13]
    }