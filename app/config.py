from pydantic import BaseSettings

#below shows use of pydantic to validate env variables
class Settings(BaseSettings):
    database_hostname: str
    database_port: str  #old code had the url as a string
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()