def user_schema(user: dict) -> dict:
    return {
        "id_usuario": user["id_usuario"],
        "rut": user["rut"],
        "nombre_usuario": user["nombre_usuario"],
        "apellidos_usuario": user["apellido_usuario"],
        "email": user["email"],
        "contrasena": user["contrasena"],
        "salt": user["salt"],
        "rol": user["rol"],
        "id_productor": user["id_productor"],
        "id_comerciante": user["id_comerciante"]
    }