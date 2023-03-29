from pydantic import BaseSettings

class Settings(BaseSettings):
  app_name: str = "Portafolio"
  db_password: str
  db_public_ip: str
  db_sid: str
  secret_key: str
  access_token_expire_days: int
  algorithm: str

  class Config:
    env_file = ".env"

settings = Settings()