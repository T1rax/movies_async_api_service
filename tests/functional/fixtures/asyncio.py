import pytest
import asyncio

from utils.helpers import Async_helper


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def async_helper(event_loop, test_config):
    return Async_helper(event_loop, test_config)