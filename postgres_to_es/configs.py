from pydantic import BaseSettings, Field


class PostgresSettings(BaseSettings):
    dbname: str = Field('movies_db', env='POSTGRES_DB')
    user: str = Field('app', env='POSTGRES_USER')
    password: str = Field('123qwe', env='POSTGRES_PASSWORD')
    host: str = Field('127.0.0.1', env='DB_HOST')
    port: str = Field(5432, env='DB_PORT')
    options: str = '-c search_path=content'

    class Config:
        env_file = './../.env'
        env_file_encoding = 'utf-8'


class ElasticSettings(BaseSettings):
    hosts: str = Field('http://localhost:9200', env='ELASTIC_ADDRESS')

    class Config:
        env_file = './../.env'
        env_file_encoding = 'utf-8'


class BaseConfig(BaseSettings):
    batch_size: int = Field(100, env='BATCH_SIZE')
    sleep_time: float = Field(10.0, env='ETL_SLEEP')
    elastic_dsn: ElasticSettings = ElasticSettings()
    postgres_dsn: PostgresSettings = PostgresSettings()

    class Config:
        env_file = './../.env'
        env_file_encoding = 'utf-8'
