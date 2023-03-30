import pytest
import pytest_asyncio
from redis.asyncio import Redis

from utils.helpers import Redis_helper
from settings import test_settings


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