import elasticsearch, redis
from pydantic import BaseSettings, Field


class MainConfig(BaseSettings):
    """ Project settings """
    LOG_LEVEL: str = Field('INFO', env='LOG_LEVEL')
    EXCEPTS: tuple = (redis.exceptions.ConnectionError,
                      redis.exceptions.TimeoutError,
                      elasticsearch.ConnectionError,
                      elasticsearch.ConnectionTimeout)

    class Config:
        env_file = './../.env'
        env_file_encoding = 'utf-8'


class RedisConfig(BaseSettings):
    """ Redis settings """
    REDIS_HOST: str = Field('127.0.0.1', env='REDIS_HOST')
    REDIS_PORT: int = Field(6379, env='REDIS_PORT')
    REDIS_CACHE: int = Field(60 * 5, env='REDIS_CACHE')  # 5 minutes

    class Config:
        env_file = './../.env'
        env_file_encoding = 'utf-8'


class ElasticConfig(BaseSettings):
    """ Elastic settings """
    ELASTIC_HOST: str = Field('127.0.0.1', env='ELASTIC_HOST')
    ELASTIC_PORT: int = Field(9200, env='ELASTIC_PORT')

    class Config:
        env_file = './../.env'
        env_file_encoding = 'utf-8'


class BaseConfig(BaseSettings):
    redis_config: RedisConfig = RedisConfig()
    es_config: ElasticConfig = ElasticConfig()
    main_config: MainConfig = MainConfig()


configs = BaseConfig()