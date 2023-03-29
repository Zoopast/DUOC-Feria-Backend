from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from db.models.token import Token, TokenData
from jose import JWTError, jwt
from configs import config
from db.models.user import Usuario, UsuarioInDB
from db.client import get_cursor
from db.schemas.user import user_schema, user_in_db_schema
import bcrypt
from auth.auth_bearer import JWTBearer

con, connection = get_cursor()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, bytes.fromhex(hashed_password))

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(email:str):
    user = None
    con.execute("SELECT * FROM usuario WHERE email = :email", {"email": email})
    user = con.fetchone()
    if user:
        user_dict = {}
        user_dict["id"] = user[0]
        user_dict["email"] = user[2]
        user_dict["password"] = user[3]
        user_dict["nombre"] = user[1]
        user_dict["salt"] = user[4]
        return UsuarioInDB(**user_in_db_schema(user_dict))

def authenticate_user(email: str, password: str):
    user = get_user(email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.settings.secret_key, algorithm=config.settings.algorithm)
    return encoded_jwt

def get_user_by_email(email: str):
    try:
        user = con.execute("SELECT * FROM usuario WHERE email = :email", {"email": email})
        return Usuario(**user)
    except:
        return { "error": "User not found" }

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
    responses={404: {"description": "Not found"}},
)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, config.settings.secret_key, algorithms=[config.settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.email)
    if user is None:
        raise credentials_exception
    return user


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
async def sign_up(user: UsuarioInDB):
    if type(get_user_by_email(user.email)) == Usuario:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user_dict = dict(user)
    del user_dict["id"]
    user_dict["salt"] = bcrypt.gensalt()
    user_dict["password"] = bcrypt.hashpw(user_dict["password"].encode("utf-8"), user_dict["salt"])
    con.execute("INSERT INTO usuario (nombre, email, password, salt) VALUES (:nombre, :email, :password, :salt)", user_dict)
    connection.commit()
    con.execute("SELECT * FROM usuario WHERE email = :email", {"email": user.email})
    result = con.fetchone()
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


@router.post("/usuario")
async def crear_usuario(usuario: Usuario):
    with con.cursor() as cur:
        cur.execute("INSERT INTO usuario (id, nombre, rol_id) VALUES (:id, :nombre, :rol_id)", {"id": usuario.id, "nombre": usuario.nombre, "rol_id": usuario.rol_id})
        connection.commit()
        return {"message": "Usuario creado correctamente"}

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