from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Provide sensible defaults for local development so type-checkers
    # and runtime instantiation without env variables don't fail.
    DATABASE_URL: str 
    SECRET: str 
    JWT_LIFETIME_SECONDS: int = 3600

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings() #type: ignore

