import elasticsearch, redis
from pydantic import BaseSettings, Field


class MainConfig(BaseSettings):
    """ Project settings """
    LOG_LEVEL: str = Field('INFO', env='LOG_LEVEL')
    EXCEPTS: tuple = (redis.exceptions.ConnectionError,
                      redis.exceptions.TimeoutError,
                      elasticsearch.ConnectionError,
                      elasticsearch.ConnectionTimeout)
    MAX_TIME: int = 60 * 10

    class Config:
        env_file = './../.env'
        env_file_encoding = 'utf-8'


class CacheConfig(BaseSettings):
    """ Redis settings """
    CACHE_HOST: str = Field('127.0.0.1', env='CACHE_HOST')
    CACHE_PORT: int = Field(6379, env='CACHE_PORT')
    CACHE_EXP: int = Field(60 * 5, env='CACHE_EXP')  # 5 minutes

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
    cache_config: CacheConfig = CacheConfig()
    es_config: ElasticConfig = ElasticConfig()
    main_config: MainConfig = MainConfig()


configs = BaseConfig()