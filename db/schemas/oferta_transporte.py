def oferta_tuple_to_dict(oferta: tuple):
    return {
				"id_oferta_transporte": oferta[0],
				"id_subasta": oferta[1],
				"id_transportista": oferta[2],
				"precio": oferta[3],
				"fecha_recoleccion": oferta[4],
				"fecha_entrega": oferta[5],
        "transportista": oferta[6] + " " + oferta[7]
		}