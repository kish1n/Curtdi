from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DISCORD_TOKEN: str
    COMMAND_PREFIX: str
    ID_SERVER: int

    CHANNEL_ID_WELCOME: int
    CHANNEL_ID_TWITCH: int
    CHANNEL_ID_TWITCH_LINK: int
    CHANNEL_ID_DOTA_LINK: int
    CHANNEL_ID_DATING: int

    TWITCH_CLIENT_ID: str
    TWITCH_CLIENT_SECRET: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()