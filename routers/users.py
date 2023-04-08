from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm
from db.models.token import Token
from configs import config
from db.models.user import Usuario
from db.client import get_cursor
import bcrypt
from auth.auth_bearer import JWTBearer
from utils.usuarios import authenticate_user, create_access_token, get_user_by_email

con, connection = get_cursor()

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
    responses={404: {"description": "Not found"}},
)


# Rutas para operaciones CRUD
@router.get("/usuario/{id}")
async def obtener_usuario(id: int):
    with con.cursor() as cur:
        cur.execute("SELECT * FROM usuario WHERE id = :id", {"id": id})
        result = cur.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"id": result[0], "nombre": result[1], "rol_id": result[2]}

# create user
@router.post("/sign_up", status_code=status.HTTP_201_CREATED)
async def sign_up(user: Usuario):
    if type(get_user_by_email(user.email)) == Usuario:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user_dict = dict(user)
    user_dict["salt"] = bcrypt.gensalt()
    user_dict["contrasena"] = bcrypt.hashpw(user_dict["contrasena"].encode("utf-8"), user_dict["salt"])
    del user_dict['id_usuario']
    del user_dict['id_productor']
    del user_dict['id_comerciante']
    con.execute("""
                INSERT INTO USUARIOS(rut, nombre_usuario, apellidos_usuario, email, contrasena, salt, rol) 
                VALUES (:rut, :nombre_usuario, :apellidos_usuario, :email, :contrasena, :salt, :rol)"""
                , user_dict)
    connection.commit()
    con.execute("SELECT * FROM USUARIOS WHERE email = :email", {"email": user.email})
    con.fetchone()
    return { "status": status.HTTP_201_CREATED, "message": "User created"}

# sign in
@router.post("/sign_in", response_model=Token, status_code=status.HTTP_200_OK)
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(days=config.settings.access_token_expire_days)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.put("/usuario/{id}")
async def actualizar_usuario(id: int, usuario: Usuario):
    with con.cursor() as cur:
        cur.execute("UPDATE usuario SET nombre = :nombre, rol_id = :rol_id WHERE id = :id", {"nombre": usuario.nombre, "rol_id": usuario.rol_id, "id": id})
        connection.commit()
        return {"message": "Usuario actualizado correctamente"}

@router.delete("/usuario/{id}")
async def eliminar_usuario(id: int):
    with con.cursor() as cur:
        cur.execute("DELETE FROM usuario WHERE id = :id", {"id": id})
        con.commit()
        return {"message": "Usuario eliminado correctamente"}

@router.get("/me")
async def read_users_me(current_user: Usuario = Depends(JWTBearer())):
    return current_user