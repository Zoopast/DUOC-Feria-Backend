def subasta_tuple_to_dict(subasta: tuple):
    return {
        "id_subasta": subasta[0],
        "id_usuario": subasta[1],
        "fecha_inicio": subasta[2],
        "fecha_fin": subasta[3],
        "estado": subasta[4],
        "id_transportista": subasta[5] if subasta[5] else None,
		}