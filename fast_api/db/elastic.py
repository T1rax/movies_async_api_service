from elasticsearch import AsyncElasticsearch


async def get_elastic() -> AsyncElasticsearch:
    es: AsyncElasticsearch | None = None
    return es
