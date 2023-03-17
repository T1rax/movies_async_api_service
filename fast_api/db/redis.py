from redis.asyncio import Redis

# Функция понадобится при внедрении зависимостей
async def get_redis() -> Redis:
    try:
        redis = Redis(host='redis', port=6379)
        return redis
    except:
        return None