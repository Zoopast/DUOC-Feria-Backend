from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .auth_handler import decodeJWT
from db.client import get_cursor

cursor, connection = get_cursor()

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
      credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
      if credentials:
        if not credentials.scheme == "Bearer":
            raise HTTPException(status_code=403, detail='Invalid authentification scheme.')

        if not self.verify_jwt(credentials.credentials):
            raise HTTPException(status_code=403, detail='Invalid token or expired token.')

        if not await self.isAdmin(credentials.credentials):
            raise HTTPException(status_code=403, detail='You do not have the required permissions.')

        return credentials.credentials
      else:
         raise HTTPException(status_code=403, detail='Invalid authorization code.')

    def verify_jwt(self, token: str):
      isTokenValid: bool = False

      try:
          payload = decodeJWT(token)
      except:
         payload = None

      if payload:
         isTokenValid = True

      return isTokenValid

    async def isAdmin(self, token: str):
      user = cursor.execute("SELECT * FROM usuario WHERE id = :id", {"id": self.get_jwt_subject(token)})
      user = user.fetchone()
      return "admin" in user["roles"]

    def get_jwt_subject(self, token: str):
      try:
          payload = decodeJWT(token)
      except:
         payload = None

      if payload:
         return payload["sub"]

      return None