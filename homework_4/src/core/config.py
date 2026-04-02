from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "dev"
    app_version: str = "1.0.0"

    db_host: str
    db_port: str
    db_user: str
    db_pass: str
    db_name: str

    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "task-avatars"
    minio_secure: bool = False
    
    secret_key: str
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    

settings = Settings()

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.db_user}:{settings.db_pass}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)
