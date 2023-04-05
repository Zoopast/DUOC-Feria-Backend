def producto_schema(producto: list) -> list:
    return {
    "id_producto": producto["id_producto"],
    "id_productor": producto["id_productor"], 
    "nombre": producto["nombre"],
    "tipo": producto["tipo"], 
    "imagen": producto["imagen"], 
    "calidad": producto["calidad"],
    "cantidad": producto["cantidad"],
    "precio": producto["precio"]
    }