def user_schema(user: dict) -> dict:
    return {
        "id_usuario": user["id_usuario"],
        "rut": user["rut"],
        "nombre_usuario": user["nombre_usuario"],
        "apellidos_usuario": user["apellidos_usuario"],
        "email": user["email"],
        "contrasena": user["contrasena"],
        "salt": user["salt"],
        "rol": user["rol"],
        "activo": user["activo"]
    }

def user_profile_schema(user: dict) -> dict:
    return {
        "id_usuario": user["id_usuario"],
        "rut": user["rut"],
        "nombre_usuario": user["nombre_usuario"],
        "apellidos_usuario": user["apellido_usuario"],
        "email": user["email"],
        "rol": user["rol"],
        "activo": user["activo"]
    }

def user_tuple_to_dict(user: tuple):
    return {
        "id_usuario": user[0],
        "rut": user[1],
        "nombre_usuario": user[2],
        "apellidos_usuario": user[3],
        "contrasena": user[4],
        "salt": user[5],
        "email": user[6],
        "rol": user[7],
        "activo": user[8]
    }