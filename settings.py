from functools import cached_property, lru_cache

# from aiokafka import AIOKafkaProducer
# from elasticsearch import AsyncElasticsearch
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from redis import Redis


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    debug_mode: bool = True

    #  data from .env file
    API_VERSION: str = "v1"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRES_HOST: str

    REDIS_HOST: str
    REDIS_PORT: str = "6379"
    REDIS_PASSWORD: str

    # KAFKA_HOST: str
    # KAFKA_PORT: str

    # ELASTIC_USER: str
    # ELASTIC_PASSWORD: str
    # ELASTIC_DOMAIN: str
    # ELASTIC_PORT: str
    # INDEX_ES_CHAT: str

    @cached_property
    def postgres_dsn(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @cached_property
    def engine(self):
        return create_async_engine(self.postgres_dsn)

    @cached_property
    def session_db(self):
        return async_sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine, class_=AsyncSession
        )

    @cached_property
    def redis(self):
        return Redis(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            decode_responses=True,
            password=self.REDIS_PASSWORD,
        )

    # @cached_property
    # def kafka_queue(self):
    #     return AIOKafkaProducer(
    #         bootstrap_servers=f"{self.KAFKA_HOST}:{self.KAFKA_PORT}"
    #     )

    # @cached_property
    # def es(self):
    #     return AsyncElasticsearch(
    #         hosts=[f"{self.ELASTIC_DOMAIN}:{self.ELASTIC_PORT}"],
    #         http_auth=(self.ELASTIC_USER, self.ELASTIC_PASSWORD),
    #         timeout=30,
    #         verify_certs=False,
    #         ssl_show_warn=False,
    #     )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
