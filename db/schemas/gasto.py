def gasto_schema(gasto: list) -> list:
    return {
        "id_gasto": gasto["id_gasto"],
        "id_proceso_venta": gasto["id_proceso_venta"],
        "tipo": gasto["tipo"],
        "monto": gasto["monto"],
        "fecha": gasto["fecha"]
    }