def transporte_schema(transporte: list) -> list:
    return {
        "id_transporte": transporte["id_transporte"],
        "id_productor": transporte["id_productor"], 
        "id_comerciante": transporte["id_comerciante"], 
        "fecha_recoleccion": transporte["fecha_recoleccion"], 
        "fecha_entrega": transporte["fecha_entrega"], 
        "costo": transporte["costo"]        
    }