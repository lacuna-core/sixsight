from dotenv import load_dotenv
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="SIXSIGHT_", env_file=".env", extra="ignore", frozen=True
    )

    toronto_open_data_base_url: AnyHttpUrl = AnyHttpUrl(
        "https://ckan0.cf.opendata.inter.prod-toronto.ca"
    )
    request_timeout: float = 30.0
    cache_dir: str = ".cache"
    log_level: str = "INFO"


SETTINGS = Settings()
