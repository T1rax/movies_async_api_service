from pydantic import BaseSettings, Field
from abc import ABC, abstractmethod


class TestSettings(BaseSettings, ABC):
    
    es_index: str = Field('movies')  
    es_index_mapping: str = Field('mappigns') 

    es_url: str = Field('http://127.0.0.1:9200', env='ELASTIC_ADDRESS')
    es_id_field: str = Field('id', env='ELASTIC_ID_FIELD')

    redis_host: str = Field('127.0.0.1', env='REDIS_HOST')
    redis_port: str = Field('6379', env='REDIS_PORT')
    service_url: str =Field('http://127.0.0.1:8000', env='SERVICE_ADDRESS')

class FilmSettings(TestSettings):
     es_index: str = Field('movies')  
     es_index_mapping: str = Field('mappigns')  
 

test_settings = TestSettings()
film_settings = FilmSettings()