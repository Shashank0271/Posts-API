from pydantic import BaseSettings

class Settings(BaseSettings):
    user_name : str
    password : str
    host_name : str
    port_number : str
    database_name : str
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int

    class Config:
        env_file = ".env"

settings = Settings()

