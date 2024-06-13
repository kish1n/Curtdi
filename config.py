from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DISCORD_TOKEN: str
    COMMAND_PREFIX: str
    ID_SERVER: int

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()