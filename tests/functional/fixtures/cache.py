import pytest
import pytest_asyncio
from redis.asyncio import Redis

from utils.helpers import Cache_helper
from settings import test_settings


@pytest_asyncio.fixture(scope='session')
async def cache_client():
    client = Redis(host=test_settings.cache_host, port=test_settings.cache_port)
    yield client
    await client.close()

@pytest.fixture(scope='session')
async def cache_clear_cache(cache_client):
    cache_helper = Cache_helper(cache_client, test_settings)

    await cache_helper.clear_cache()

@pytest.fixture
def cache_helper(cache_client):
    return Cache_helper(cache_client, test_settings)