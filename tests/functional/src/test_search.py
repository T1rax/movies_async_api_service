import pytest
import json
from http import HTTPStatus

from settings import test_settings


@pytest.mark.parametrize(
    'test_config, query_data, expected_answer',
    [
        (
                test_settings,
                {'query': 'The Star'},
                {'status': HTTPStatus.OK, 'length': 50}
        ),
        (
                test_settings,
                {'query': 'Mashed potato'},
                {'status': HTTPStatus.NOT_FOUND, 'length': 0}
        )
    ]
)
@pytest.mark.asyncio
async def test_films_search(query_data, expected_answer, prepare_film_es, cache_clear_cache, aiohttp_helper):

    # 1. Генерируем данные и загружаем данные в ES (запускается 1 раз для всех тестов)
    try:
        await prepare_film_es
    except RuntimeError:
        prepare_film_es
    
    # 2. Чистим кеш редиса (запускается 1 раз для всех тестов)
    try:
        await cache_clear_cache
    except RuntimeError:
        cache_clear_cache

    # 3. Запрашиваем данные из ES по API
    status, array_length, body, headers = await aiohttp_helper.make_get_request(test_settings.service_url, '/api/v1/films/search', query_data)

    # 4. Проверяем ответ 
    assert status == expected_answer['status']
    assert array_length == expected_answer['length']


@pytest.mark.parametrize(
    'test_config, parameters, expected_answer',
    [
        (
                test_settings,
                {'query': 'Edd'},
                {'status': HTTPStatus.OK, 'length': 1}
        ),
        (
                test_settings,
                {'query': 'Tom'},
                {'status': HTTPStatus.NOT_FOUND, 'length': 0}
        )
    ]
)
@pytest.mark.asyncio
async def test_persons_search(parameters, expected_answer, prepare_person_es, cache_clear_cache, aiohttp_helper):
    # 1. Генерируем данные и загружаем данные в ES (запускается 1 раз для всех тестов)
    try:
        await prepare_person_es
    except RuntimeError:
        prepare_person_es

    # 2. Чистим кеш редиса (запускается 1 раз для всех тестов)
    try:
        await cache_clear_cache
    except RuntimeError:
        cache_clear_cache

    # 3. Запрашиваем данные из ES по API
    status, array_length, body, headers = await aiohttp_helper.make_get_request(test_settings.service_url,
                                                                                '/api/v1/persons/search', parameters)

    # 4. Проверяем ответ
    assert status == expected_answer['status']
    assert array_length == expected_answer['length']


@pytest.mark.parametrize(
    'test_config, parameters, expected_answer',
    [
        (
                test_settings,
                {'query': 'Edd', 'page_number': 1, 'page_size': 50},
                {'status': HTTPStatus.OK, 'length': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_persons_search_cache(parameters, expected_answer, prepare_person_es, cache_clear_cache, aiohttp_helper, cache_helper):
    # 1. Генерируем данные и загружаем данные в ES (запускается 1 раз для всех тестов)
    try:
        await prepare_person_es
    except RuntimeError:
        prepare_person_es

    # 2. Чистим кеш редиса (запускается 1 раз для всех тестов)
    try:
        await cache_clear_cache
    except RuntimeError:
        cache_clear_cache

    # 3. Запрашиваем данные из ES по API
    status, array_length, body, headers = await aiohttp_helper.make_get_request(test_settings.service_url,
                                                                                '/api/v1/persons/search', parameters)

    # 4. Проверяем наличие в редисе
    cache_value = await cache_helper.get_value(
        'get_by_search___None___None___None___'+parameters.get('query')+'___None___'+str(parameters.get('page_number'))+'___'+str(parameters.get('page_size'))+'___None')
    cache_value = len(json.loads(cache_value))

    # 5. Проверяем ответ
    assert status == expected_answer['status']
    assert cache_value == expected_answer['length']