import elasticsearch, redis
from pydantic import BaseSettings, Field


class MainConfig(BaseSettings):
    """ Project settings """
    log_level: str = Field('INFO', env='LOG_LEVEL')
    excepts: tuple = (redis.exceptions.ConnectionError,
                      redis.exceptions.TimeoutError,
                      elasticsearch.ConnectionError,
                      elasticsearch.ConnectionTimeout)
    max_time: int = 60 * 10
    default_page_number: int = 1
    default_page_size: int = 50

    class Config:
        env_file = './../.env'
        env_file_encoding = 'utf-8'


class RedisConfig(BaseSettings):
    """ Redis settings """
    redis_host: str = Field('127.0.0.1', env='REDIS_HOST')
    redis_port: int = Field(6379, env='REDIS_PORT')
    redis_cache: int = Field(60 * 5, env='REDIS_CACHE')  # 5 minutes

    class Config:
        env_file = './../.env'
        env_file_encoding = 'utf-8'


class ElasticConfig(BaseSettings):
    """ Elastic settings """
    elastic_host: str = Field('127.0.0.1', env='ELASTIC_HOST')
    elastic_port: int = Field(9200, env='ELASTIC_PORT')

    class Config:
        env_file = './../.env'
        env_file_encoding = 'utf-8'


class BaseConfig(BaseSettings):
    redis_config: RedisConfig = RedisConfig()
    es_config: ElasticConfig = ElasticConfig()
    main_config: MainConfig = MainConfig()


configs = BaseConfig()