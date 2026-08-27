# src/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    snowflake_account: str
    snowflake_user: str
    snowflake_private_key_path: str
    snowflake_database: str
    snowflake_schema: str
    snowflake_warehouse: str
    snowflake_role: str = "ACCOUNTADMIN" # Default fallback

    # This tells Pydantic to look for the .env file in the root
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Instantiate the settings once so they can be imported across your app
settings = Settings()