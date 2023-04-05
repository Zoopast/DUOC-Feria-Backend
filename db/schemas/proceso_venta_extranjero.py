def proceso_venta_extranjero_schema(proceso_venta_extranjero: list) -> list:
    return {
        "id_proceso_venta": proceso_venta_extranjero["id_proceso_venta"],
        "id_contrato": proceso_venta_extranjero["id_contrato"],
        "fecha_inicio": proceso_venta_extranjero["fecha_inicio"], 
        "fecha_fin": proceso_venta_extranjero["fecha_fin"],
        "precio_venta": proceso_venta_extranjero["precio_venta"],
        "cantidad_producto": proceso_venta_extranjero["cantidad_producto"]    
    }