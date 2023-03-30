import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from utils.helpers import Elastic_helper
from testdata.es_mapping import Elastic_mock
from settings import test_settings, film_settings, genre_settings, person_settings


@pytest_asyncio.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=test_settings.es_url)
    yield client
    await client.close()

@pytest.fixture(scope='session')
async def prepare_film_es(es_client):
    es_helper = Elastic_helper(es_client, film_settings)
    es_mock = Elastic_mock()

    #Данные для тестов фильмов
    await es_helper.delete_index()
    await es_helper.create_index()
    await es_helper.es_write_data(es_mock.generate_film_data(53))
    await es_helper.es_write_data(es_mock.generate_film_with_id())
    await es_helper.es_write_data(es_mock.generate_film_with_id('redisccachetest-5a1c-4b95-b32b-fdd89b40dddc'))
    await es_helper.check_index()

    return es_helper

@pytest.fixture(scope='session')
async def prepare_genre_es(es_client):
    es_helper = Elastic_helper(es_client, genre_settings)
    es_mock = Elastic_mock()

    #Данные для тестов фильмов
    await es_helper.delete_index()
    await es_helper.create_index()
    await es_helper.es_write_data(es_mock.generate_genre_data())
    await es_helper.check_index()

    return es_helper

@pytest.fixture(scope='session')
async def prepare_person_es(es_client):
    es_helper = Elastic_helper(es_client, person_settings)
    es_mock = Elastic_mock()

    #Данные для тестов фильмов
    await es_helper.delete_index()
    await es_helper.create_index()
    await es_helper.es_write_data(es_mock.generate_person_data())
    await es_helper.check_index()

    return es_helper