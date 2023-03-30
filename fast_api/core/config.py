import elasticsearch, redis
from pydantic import BaseSettings, Field


class MainConfig(BaseSettings):
    """ Project settings """
    log_level: str = Field('INFO')
    excepts: tuple = (redis.exceptions.ConnectionError,
                      redis.exceptions.TimeoutError,
                      elasticsearch.ConnectionError,
                      elasticsearch.ConnectionTimeout)
    max_time: int = 60 * 10
    default_page_number: int = 1
    default_page_size: int = 50


class CacheConfig(BaseSettings):
    """ Cache settings """
    host: str = Field('127.0.0.1')
    port: int = Field(6379)
    exp: int = Field(60 * 5)  # 5 minutes


class ElasticConfig(BaseSettings):
    """ Elastic settings """
    host: str = Field('127.0.0.1')
    port: int = Field(9200)


class BaseConfig(BaseSettings):
    cache: CacheConfig = CacheConfig()
    elastic: ElasticConfig = ElasticConfig()
    cfg: MainConfig = MainConfig()

    class Config:
        env_prefix = 'API_'
        env_nested_delimiter = '__'
        env_file = './../.env'
        env_file_encoding = 'utf-8'


configs = BaseConfig()