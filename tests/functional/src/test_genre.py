import pytest
import json
from http import HTTPStatus

from settings import test_settings


@pytest.mark.parametrize(
    'test_config, genre_id, expected_answer',
    [
        (
                test_settings,
                'genre-id-1',
                {'status': HTTPStatus.OK, 'id': 'genre-id-1'}
        ),
        (
                test_settings,
                'genre-id-123',
                {'status': HTTPStatus.NOT_FOUND, 'id': None}
        ),
        (
                test_settings,
                '12334',
                {'status': HTTPStatus.NOT_FOUND, 'id': None}
        ),
    ]
)
@pytest.mark.asyncio
async def test_genre_id(test_config, genre_id, expected_answer, prepare_genre_es, cache_clear_cache, aiohttp_helper):

    # 1. Генерируем данные и загружаем данные в ES (запускается 1 раз для всех тестов)
    try:
        await prepare_genre_es
    except RuntimeError:
        prepare_genre_es
    
    # 2. Чистим кеш редиса (запускается 1 раз для всех тестов)
    try:
        await cache_clear_cache
    except RuntimeError:
        cache_clear_cache

    # 3. Запрашиваем данные из ES по API
    status, array_length, body, headers = await aiohttp_helper.make_get_request(test_config.service_url, '/api/v1/genres/'+genre_id)

    # 4. Проверяем ответ 
    assert status == expected_answer['status']
    assert body.get('id') == expected_answer['id'] 


@pytest.mark.parametrize(
    'test_config, genre_id, expected_answer',
    [
        (
                test_settings,
                'genre-id-1',
                {'status': HTTPStatus.OK, 'id': 'genre-id-1'}
        ),
    ]
)
@pytest.mark.asyncio
async def test_genre_id_cache(test_config, genre_id, expected_answer, prepare_genre_es, cache_clear_cache, aiohttp_helper, cache_helper):

    # 1. Генерируем данные и загружаем данные в ES (запускается 1 раз для всех тестов)
    try:
        await prepare_genre_es
    except RuntimeError:
        prepare_genre_es
    
    # 2. Чистим кеш редиса (запускается 1 раз для всех тестов)
    try:
        await cache_clear_cache
    except RuntimeError:
        cache_clear_cache

    # 3. Запрашиваем данные из ES по API
    status, array_length, body, headers = await aiohttp_helper.make_get_request(test_config.service_url, '/api/v1/genres/'+genre_id)

    # 4. Проверяем наличие ключа в редисе
    cache_value = await cache_helper.get_value('get_by_id___None___'+genre_id+'___None___None___None___None___None___None')
    cache_value = json.loads(cache_value)
    cache_value['id'] = cache_value.pop('uuid')

    # 5. Проверяем ответ 
    assert status == expected_answer['status']
    assert body.get('id') == expected_answer['id'] 
    assert cache_value == body


@pytest.mark.parametrize(
    'test_config, expected_answer',
    [
        (
                test_settings,
                {'status': HTTPStatus.OK, 'length': 5}
        ),
    ]
)
@pytest.mark.asyncio
async def test_genre_all_genres(test_config, expected_answer, prepare_genre_es, cache_clear_cache, aiohttp_helper):

    # 1. Генерируем данные и загружаем данные в ES (запускается 1 раз для всех тестов)
    try:
        await prepare_genre_es
    except RuntimeError:
        prepare_genre_es
    
    # 2. Чистим кеш редиса (запускается 1 раз для всех тестов)
    try:
        await cache_clear_cache
    except RuntimeError:
        cache_clear_cache

    # 3. Запрашиваем данные из ES по API
    status, array_length, body, headers = await aiohttp_helper.make_get_request(test_config.service_url, '/api/v1/genres/')

    # 4. Проверяем ответ 
    assert status == expected_answer['status']
    assert array_length == expected_answer['length'] 


@pytest.mark.parametrize(
    'test_config, expected_answer',
    [
        (
                test_settings,
                {'status': HTTPStatus.OK, 'length': 5}
        ),
    ]
)
@pytest.mark.asyncio
async def test_genre_all_genres_cache(test_config, expected_answer, prepare_genre_es, cache_clear_cache, aiohttp_helper, cache_helper):

    # 1. Генерируем данные и загружаем данные в ES (запускается 1 раз для всех тестов)
    try:
        await prepare_genre_es
    except RuntimeError:
        prepare_genre_es
    
    # 2. Чистим кеш редиса (запускается 1 раз для всех тестов)
    try:
        await cache_clear_cache
    except RuntimeError:
        cache_clear_cache

    # 3. Запрашиваем данные из ES по API
    status, array_length, body, headers = await aiohttp_helper.make_get_request(test_config.service_url, '/api/v1/genres/')

    # 4. Проверяем наличие ключа в редисе
    cache_value = await cache_helper.get_value('get_genres___None___None___None___None___None___None___None___None')
    cache_value = json.loads(cache_value)
    for i in range(len(cache_value)):
        cache_value[i] = json.loads(cache_value[i])

    # 5. Проверяем ответ 
    assert status == expected_answer['status']
    assert array_length == expected_answer['length'] 
    assert cache_value == body