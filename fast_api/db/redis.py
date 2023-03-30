from core.config import configs
from redis.asyncio import Redis


async def get_redis() -> Redis:
    try:
        redis = Redis(host=configs.cache_config.cache_host, port=configs.cache_config.cache_port)
        return redis
    except:
        return None




