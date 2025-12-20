from pydantic_settings import BaseSettings, SettingsConfigDict

from src.common.constants.paths import BASE_DIR


class Settings(BaseSettings):
    # Backend
    sqlalchemy_echo: bool = True

    # Database
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int

    @property
    def postgresql_url(self) -> str:
        return (
            f'postgresql+asyncpg://'
            f'{self.postgres_user}:'
            f'{self.postgres_password}@'
            f'{self.postgres_host}:'
            f'{self.postgres_port}/'
            f'{self.postgres_db}'
        )

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


config: Settings = Settings()
