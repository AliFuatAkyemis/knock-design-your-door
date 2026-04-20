from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    groq_api_key: str
    max_upload_size_mb: int = 25
    upload_dir: str = "uploads"
    output_dir: str = "outputs"
    frontend_origin: str = "http://localhost:8000"

    class Config:
        env_file = ".env"


settings = Settings()
