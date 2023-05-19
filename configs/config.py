from pydantic import BaseSettings
from functools import lru_cache
class Settings(BaseSettings):
  app_name: str = "Portafolio"
  db_port: int
  db_password: str
  db_public_ip: str
  db_sid: str
  secret_key: str
  access_token_expire_days: int
  algorithm: str
  db_user: str

  class Config:
    env_file = ".env"


@lru_cache()
def get_settings():
  return Settings()