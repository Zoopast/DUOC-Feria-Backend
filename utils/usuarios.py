from fastapi import Depends, HTTPException, status
from db.schemas.user import user_schema
from fastapi.security import OAuth2PasswordBearer
from db.client import get_cursor
from passlib.context import CryptContext
from db.models.user import Usuario
from datetime import datetime, timedelta
from configs import config
from jose import JWTError, jwt
from db.models.token import TokenData

con, connection = get_cursor()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, bytes.fromhex(hashed_password))

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(email:str):
    user = None
    con.execute("SELECT * FROM USUARIOS WHERE email = :email", { "email": email })
    user = con.fetchone()
    if user:
        user_dict = {}
        user_dict["id"] = user[0]
        user_dict["rut"] = user[1]
        user_dict["nombre_usuario"] = user[2]
        user_dict["apellidos_usuario"] = user[3]
        user_dict["email"] = user[2]
        user_dict["password"] = user[3]
        user_dict["salt"] = user[4]
        user_dict["rol"] = user[5]
        user_dict["id_productor"] = user[6]
        user_dict["id_comerciante"] = user[7]
        return Usuario(**user_schema(user_dict))

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
        user = con.execute("SELECT * FROM USUARIOS WHERE email = :email", {"email": email})
        return Usuario(**user)
    except:
        return { "error": "User not found" }

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