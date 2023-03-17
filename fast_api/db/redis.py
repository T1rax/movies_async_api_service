from core import config
from redis.asyncio import Redis


async def get_redis() -> Redis:
    try:
        redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
        return redis
    except:
        return None