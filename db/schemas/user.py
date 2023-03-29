def user_schema(user: dict) -> dict:
    return {
        "id": user["id"],
        "nombre": user["nombre"],
        "email": user["email"],
    }

def user_in_db_schema(user: dict) -> dict:
    return {
        "id": user["id"],
        "nombre": user["nombre"],
        "email": user["email"],
        "password": user["password"],
        "salt": user["salt"]
    }