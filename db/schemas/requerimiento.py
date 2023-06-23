def requerimiento_tuple_to_dict(requerimiento: tuple, productos: list = [], usuario: dict = {}):
    return {
				"id_requerimiento": requerimiento[0],
        "fecha_inicio": requerimiento[1],
        "fecha_fin": requerimiento[2],
        "usuario": usuario,
				"estado": requerimiento[4],
        "direccion": requerimiento[5],
				"productos": productos,
		}

def requerimiento_oferta_tuple_to_dict(oferta: tuple):
    return {
        "id_requerimiento_oferta": oferta[0],
        "id_requerimiento": oferta[1],
        "id_producto_requerimiento": oferta[2],
        "id_productor": oferta[3],
        "cantidad": int(oferta[4]),
        "precio": int(oferta[5]),
    }