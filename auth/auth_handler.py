from jose import jwt
from configs.config import settings
import time

def decodeJWT(token: str) -> dict:
  try:
    decoded_token = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    return decoded_token if decoded_token["exp"] >= time.time() else None
  except:
    return {}