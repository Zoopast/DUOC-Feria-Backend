def productor_schema(productor: tuple) -> list:
    return {
        "id_productor": productor[0],
        "nombre": productor[1],
        "email": productor[2],
        "telefono": productor[3],
        "direccion": productor[4],
        "id_usuario": productor[5]
    }