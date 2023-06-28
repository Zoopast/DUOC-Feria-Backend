def producto_tuple_to_dict(producto):
		return {
				"id_producto": producto[0],
				"nombre": producto[1],
				"cantidad": producto[2],
				"calidad": producto[4],
		}

def producto_subasta_tuple_to_dict(producto):
		return {
				"id_producto": producto[0],
				"nombre": producto[1],
				"cantidad": producto[2],
				"calidad": producto[4],
				"direccion": producto[5],
		}