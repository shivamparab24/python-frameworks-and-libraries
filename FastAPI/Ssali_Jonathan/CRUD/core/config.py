from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    database_url: str = None

    jwt_secret: str = None
    jwt_algorithm: str = None

    # redis_host: str = "localhost"
    # redis_port: int = 6379

    redis_url: str 

    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int = 587
    mail_server: str
    mail_from_name: str

    mail_starttls: bool = True
    mail_ssl_tls: bool = False
    use_credentials: bool = True
    validate_certs: bool = True

    domain: str


    model_config = SettingsConfigDict(
        env_file = ".env",
        extra = "ignore"
    )
    

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
 
settings = get_settings()

broker_url = settings.redis_url
result_backend = settings.redis_url
broker_connection_retry_on_startup = True 