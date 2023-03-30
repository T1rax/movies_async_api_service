#Imports for local testing
import sys
sys.path.insert(0, '/home/tirax/movies_async_api_service/tests/functional')
sys.path.insert(0, '/home/seo/proj/sprint_5/movies_async_api_service/tests/functional')


pytest_plugins = ('fixtures.elasticsearch',
                  'fixtures.asyncio',
                  'fixtures.cache',
                  'fixtures.aiohttp')
