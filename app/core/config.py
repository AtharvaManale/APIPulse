from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_host : str
    db_port : int
    db_user : str
    db_password : str
    db_name : str

    jwt_secret_key : str
    jwt_algorithm : str
    access_token_expire_minutes : int

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()