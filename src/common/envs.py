from pydantic_settings import BaseSettings, SettingsConfigDict

from src.common.constants.paths import BASE_DIR


class EnvConfig(BaseSettings):
    # Backend
    sqlalchemy_echo: bool = True
    jwt_secret_key: str = 'local-secret'
    jwt_expiration_minutes: int = 30

    # Database
    postgres_user: str = 'local_user'
    postgres_password: str = 'local_password'
    postgres_db: str = 'orders_db'
    postgres_host: str = 'localhost'
    postgres_port: int = 5432

    # Kafka
    kafka_host: str = 'localhost'
    kafka_port: int = 9094

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

    @property
    def kafka_bootstrap_servers(self) -> str:
        return f'{self.kafka_host}:{self.kafka_port}'

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


env_config: EnvConfig = EnvConfig()
