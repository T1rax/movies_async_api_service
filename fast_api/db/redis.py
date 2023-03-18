from core.config import RedisConfig
from redis.asyncio import Redis


async def get_redis() -> Redis:
    try:
        redis = Redis(host=RedisConfig().REDIS_HOST, port=RedisConfig().REDIS_PORT)
        return redis
    except:
        return None