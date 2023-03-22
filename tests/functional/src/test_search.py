import sys
sys.path.insert(0, '/home/tirax/movies_async_api_service/tests/functional')
sys.path.insert(0, '/opt/app')

import datetime
import uuid
import json

import aiohttp
import pytest

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, async_bulk

from settings import test_settings
# from ..utils.helpers import es_write_data

#  Название теста должно начинаться со слова `test_`
#  Любой тест с асинхронными вызовами нужно оборачивать декоратором `pytest.mark.asyncio`, который следит за запуском и работой цикла событий. 


@pytest.mark.parametrize(
    'test_config, query_data, expected_answer',
    [
        (
                test_settings,
                {'query': 'The Star'},
                {'status': 200, 'length': 50}
        ),
        (
                test_settings,
                {'search': 'Mashed potato'},
                {'status': 404, 'length': 0}
        )
    ]
)
@pytest.mark.asyncio
async def test_search(query_data, expected_answer, es_helper):

    # 1. Генерируем данные для ES

    es_data = [{
        'id': str(uuid.uuid4()),
        'imdb_rating': 8.5,
        'genre': ['Action', 'Sci-Fi'],
        'title': 'The Star',
        'description': 'New World',
        'director': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': '111', 'name': 'Ann'},
            {'id': '222', 'name': 'Bob'}
        ],
        'writers': [
            {'id': '333', 'name': 'Ben'},
            {'id': '444', 'name': 'Howard'}
        ],
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat(),
        'film_work_type': 'movie'
    } for _ in range(60)]

    # 2. Загружаем данные в ES

    await es_helper.es_write_data(es_data)
    
    # 3. Запрашиваем данные из ES по API

    session = aiohttp.ClientSession()
    url = test_settings.service_url + '/api/v1/films/search'
    async with session.get(url, params=query_data) as response:
        body = await response.json()
        headers = response.headers
        status = response.status
    await session.close()

    # print(response)

    if isinstance(body, list):
        length = len(body)
    else:
        length = 0

    # 4. Проверяем ответ 

    assert status == expected_answer['status']
    assert length == expected_answer['length'] 



# async def test_search(make_get_request, es_write_data, es_data: List[dict], query_data: dict, expected_answer: dict):
#     await es_write_data(es_data)
#     response = await make_get_request('/search', query_data)
#     # Дальше идут проверки ответа API