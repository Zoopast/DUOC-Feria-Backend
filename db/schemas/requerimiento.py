def requerimiento_tuple_to_dict(requerimiento: tuple, productos: list = [], usuario: dict = {}):
    return {
				"id_requerimiento": requerimiento[0],
        "fecha_inicio": requerimiento[1],
        "fecha_fin": requerimiento[2],
        "calidad": requerimiento[3],
        "usuario": usuario,
				"estado": requerimiento[5],
				"productos": productos,
		}