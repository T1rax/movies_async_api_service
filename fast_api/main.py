from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from api.v1.router import router
from core.config import RedisConfig, ElasticConfig
from core.logger import LOGGING
from db import elastic, redis


app = FastAPI(
    title="Read-only API для онлайн-кинотеатра",
    description="Информация о фильмах, жанрах и людях, участвовавших в создании произведения",
    version="1.0.0",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    redis.redis = Redis(host=RedisConfig().REDIS_HOST, port=RedisConfig().REDIS_PORT)
    elastic.es = AsyncElasticsearch(hosts=[f'{ElasticConfig().ELASTIC_HOST}:{ElasticConfig().ELASTIC_PORT}'])


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(router, prefix='/api/v1')