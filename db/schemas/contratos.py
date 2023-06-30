def contrato_tuple_to_dict(contrato: tuple) -> dict:
    return {
        "id_contrato": contrato[0],
        "id_cliente": contrato[1],
        "id_transportista": contrato[2],
        "id_requerimiento": contrato[3],
		}