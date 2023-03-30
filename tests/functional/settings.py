from pydantic import BaseSettings, Field

from testdata.es_index import settings, mappings_movies, mappings_genres, mappings_persons

class ServiceNotReady(Exception):
    "Raised when service is not awailable yet"
    pass


class TestSettings(BaseSettings):
    
    es_index: str = Field('movies')  
    es_index_settings: dict = Field(settings)  
    es_index_mapping: dict = Field(mappings_movies) 

    es_url: str = Field('http://127.0.0.1:9200', env='ELASTIC_ADDRESS')
    es_id_field: str = Field('id', env='ELASTIC_ID_FIELD')

    cache_host: str = Field('127.0.0.1', env='API_CACHE__HOST')
    cache_port: str = Field('6379', env='API_CACHE__PORT')
    service_url: str =Field('http://127.0.0.1:8000', env='SERVICE_ADDRESS')


class FilmSettings(TestSettings):
     es_index: str = Field('movies')  
     es_index_mapping: dict = Field(mappings_movies) 

class GenreSettings(TestSettings):
     es_index: str = Field('genres')  
     es_index_mapping: dict = Field(mappings_genres)      
 
class PersonSettings(TestSettings):
     es_index: str = Field('persons')  
     es_index_mapping: dict = Field(mappings_persons)  


test_settings = TestSettings()
film_settings = FilmSettings()
genre_settings = GenreSettings()
person_settings = PersonSettings()