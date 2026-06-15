from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    GROQ_API_KEY: str | None = None
    ELEVENLABS_API_KEY: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()