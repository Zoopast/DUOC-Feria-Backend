def venta_local_schema(venta_local: list) -> list:
    return {
        "id_venta_local": venta_local["id_venta_local"],
        "id_producto": venta_local["id_producto"],
        "id_comerciante": venta_local["id_comerciante"],
        "cantidad": venta_local["cantidad"],
        "precio_venta": venta_local["precio_venta"],
        "fecha": venta_local["fecha"]
    }