from core.config import configs
from redis.asyncio import Redis


async def get_redis() -> Redis:
    try:
        redis = Redis(host=configs.redis_config.REDIS_HOST, port=configs.redis_config.REDIS_PORT)
        return redis
    except:
        return None