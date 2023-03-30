from core.config import configs
from redis.asyncio import Redis


async def get_redis() -> Redis:
    try:
        redis = Redis(host=configs.cache.host, port=configs.cache.port)
        return redis
    except:
        return None




