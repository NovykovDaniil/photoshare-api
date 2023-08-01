from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str
    secret_key: str
    algorithm: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_password: str = 'password'
    cloudinary_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str
    openai_api_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()