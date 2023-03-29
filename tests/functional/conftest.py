#Imports for local testing
import sys
sys.path.insert(0, '/home/tirax/movies_async_api_service/tests/functional')
sys.path.insert(0, '/home/seo/proj/sprint_5/movies_async_api_service/tests/functional')

import asyncio
import aiohttp
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from utils.helpers import Elastic_helper, Redis_helper, Async_helper, Aiohttp_helper
from testdata.es_mapping import Elastic_mock
from settings import test_settings, film_settings, genre_settings, person_settings


# AsyncIO
@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def async_helper(event_loop, test_config):
    return Async_helper(event_loop, test_config)


# ElasticSearch
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


# Redis
@pytest_asyncio.fixture(scope='session')
async def redis_client():
    client = Redis(host=test_settings.redis_host, port=test_settings.redis_port)
    yield client
    await client.close()

@pytest.fixture(scope='session')
async def redis_clear_cache(redis_client):
    redis_helper = Redis_helper(redis_client, test_settings)

    await redis_helper.clear_cache()

@pytest.fixture
def redis_helper(redis_client):
    return Redis_helper(redis_client, test_settings)


# Aiohttp
@pytest_asyncio.fixture(scope='session')
async def aiohttp_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()

@pytest.fixture
def aiohttp_helper(aiohttp_session, test_config):
    return Aiohttp_helper(aiohttp_session, test_config)
