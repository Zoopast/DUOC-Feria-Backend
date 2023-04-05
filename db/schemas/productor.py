def productor_schema(productor: list) -> list:
    return {
        "id_productor": productor["id_productor"],
        "nombre": productor["nombre"],
        "email": productor["email"],
        "telefono": productor["telefono"],
        "direccion": productor["direccion"],
        "id_contrato": productor["id_contrato"]
    }