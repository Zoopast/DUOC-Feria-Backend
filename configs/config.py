from pydantic import BaseSettings

class Settings(BaseSettings):
  app_name: str = "Portafolio"
  db_password: str
  db_public_ip: str
  db_sid: str

  class Config:
    env_file = ".env"

settings = Settings()