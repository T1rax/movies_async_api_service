from core.config import configs
from redis.asyncio import Redis


async def get_redis() -> Redis:
    try:
        redis = Redis(host=configs.cache_config.CACHE_HOST, port=configs.cache_config.CACHE_PORT)
        return redis
    except:
        return None




