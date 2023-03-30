from core.config import configs
from redis.asyncio import Redis


async def get_redis() -> Redis:
    try:
        redis = Redis(host=configs.redis_config.redis_host, port=configs.redis_config.redis_port)
        return redis
    except:
        return None




