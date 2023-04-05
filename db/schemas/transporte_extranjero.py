def transporte_extranjero_schema(transporte_extranjero: list) -> list:
    return {
        "id_transporte_extranjero": transporte_extranjero["id_transporte_extranjero"],
        "id_proceso_venta": transporte_extranjero["id_proceso_venta"],
        "nombre_transportista": transporte_extranjero["nombre_transportista"],
        "fecha_salida": transporte_extranjero["fecha_salida"],
        "fecha_llegada": transporte_extranjero["fecha_llegada"],
        "costo": transporte_extranjero["costo"]
    }