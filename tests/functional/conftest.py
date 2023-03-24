import sys
sys.path.insert(0, '/home/tirax/movies_async_api_service/tests/functional')
sys.path.insert(0, '/opt/app')

from typing import List

import asyncio
import aiohttp
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from utils.helpers import Elastic_helper, Redis_helper, Async_helper, Aiohttp_helper
from testdata.es_mapping import Elastic_mock
from settings import test_settings

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

@pytest.fixture
def es_helper(es_client, test_config):
    return Elastic_helper(es_client, test_config)

@pytest.fixture
def es_mock():
    return Elastic_mock()

# Redis
@pytest_asyncio.fixture(scope='session')
async def redis_client():
    client = Redis(host=test_settings.redis_host, port=test_settings.redis_port)
    yield client
    await client.close()

@pytest.fixture
def redis_helper(redis_client, test_config):
    return Redis_helper(redis_client, test_config)

# Aiohttp
@pytest_asyncio.fixture(scope='session')
async def aiohttp_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()

@pytest.fixture
def aiohttp_helper(aiohttp_session, test_config):
    return Aiohttp_helper(aiohttp_session, test_config)
