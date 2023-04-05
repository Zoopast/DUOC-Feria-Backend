def comerciante_schema(comerciante: list) -> list:
    return {
    "id_comerciante": comerciante.id_comerciante, 
    "nombre": comerciante.nombre,
    "email": comerciante.email,
    "telefono": comerciante.telefono,
    "direccion": comerciante.direccion
    }