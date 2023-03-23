import sys
sys.path.insert(0, '/home/tirax/movies_async_api_service/tests/functional')
sys.path.insert(0, '/opt/app')

from typing import List

import asyncio
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from utils.helpers import Elastic_helper
from settings import test_settings


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=test_settings.es_url)
    yield client
    await client.close()

@pytest.fixture
def es_helper(es_client, test_config):
    return Elastic_helper(es_client, test_config)


@pytest.fixture
def make_get_request():
    async def inner(data: List[dict]):
        pass

    return inner