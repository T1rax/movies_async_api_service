import pytest
import json

from settings import test_settings


@pytest.mark.parametrize(
    'test_config, genre_id, expected_answer',
    [
        (
                test_settings,
                'genre-id-1',
                {'status': 200, 'id': 'genre-id-1'}
        ),
        (
                test_settings,
                'genre-id-123',
                {'status': 404, 'id': None}
        ),
        (
                test_settings,
                '12334',
                {'status': 404, 'id': None}
        ),
    ]
)
@pytest.mark.asyncio
async def test_genre_id(test_config, genre_id, expected_answer, prepare_genre_es, redis_clear_cache, aiohttp_helper):

    # 1. Генерируем данные и загружаем данные в ES (запускается 1 раз для всех тестов)
    try:
        await prepare_genre_es
    except RuntimeError:
        prepare_genre_es
    
    # 2. Чистим кеш редиса (запускается 1 раз для всех тестов)
    try:
        await redis_clear_cache
    except RuntimeError:
        redis_clear_cache

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
                {'status': 200, 'id': 'genre-id-1'}
        ),
    ]
)
@pytest.mark.asyncio
async def test_genre_id_redis_cache(test_config, genre_id, expected_answer, prepare_genre_es, redis_clear_cache, aiohttp_helper, redis_helper):

    # 1. Генерируем данные и загружаем данные в ES (запускается 1 раз для всех тестов)
    try:
        await prepare_genre_es
    except RuntimeError:
        prepare_genre_es
    
    # 2. Чистим кеш редиса (запускается 1 раз для всех тестов)
    try:
        await redis_clear_cache
    except RuntimeError:
        redis_clear_cache

    # 3. Запрашиваем данные из ES по API
    status, array_length, body, headers = await aiohttp_helper.make_get_request(test_config.service_url, '/api/v1/genres/'+genre_id)

    # 4. Проверяем наличие ключа в редисе
    redis_cache = await redis_helper.get_value('get_by_id___None___'+genre_id+'___None___None___None___None___None___None')
    redis_cache = json.loads(redis_cache)
    redis_cache['id'] = redis_cache.pop('uuid')

    # 5. Проверяем ответ 
    assert status == expected_answer['status']
    assert body.get('id') == expected_answer['id'] 
    assert redis_cache == body


@pytest.mark.parametrize(
    'test_config, expected_answer',
    [
        (
                test_settings,
                {'status': 200, 'length': 5}
        ),
    ]
)
@pytest.mark.asyncio
async def test_genre_all_genres(test_config, expected_answer, prepare_genre_es, redis_clear_cache, aiohttp_helper):

    # 1. Генерируем данные и загружаем данные в ES (запускается 1 раз для всех тестов)
    try:
        await prepare_genre_es
    except RuntimeError:
        prepare_genre_es
    
    # 2. Чистим кеш редиса (запускается 1 раз для всех тестов)
    try:
        await redis_clear_cache
    except RuntimeError:
        redis_clear_cache

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
                {'status': 200, 'length': 5}
        ),
    ]
)
@pytest.mark.asyncio
async def test_genre_all_genres_redis_cache(test_config, expected_answer, prepare_genre_es, redis_clear_cache, aiohttp_helper, redis_helper):

    # 1. Генерируем данные и загружаем данные в ES (запускается 1 раз для всех тестов)
    try:
        await prepare_genre_es
    except RuntimeError:
        prepare_genre_es
    
    # 2. Чистим кеш редиса (запускается 1 раз для всех тестов)
    try:
        await redis_clear_cache
    except RuntimeError:
        redis_clear_cache

    # 3. Запрашиваем данные из ES по API
    status, array_length, body, headers = await aiohttp_helper.make_get_request(test_config.service_url, '/api/v1/genres/')

    # 4. Проверяем наличие ключа в редисе
    redis_cache = await redis_helper.get_value('get_genres___None___None___None___None___None___None___None___None')
    redis_cache = json.loads(redis_cache)
    for i in range(len(redis_cache)):
        redis_cache[i] = json.loads(redis_cache[i])

    # 5. Проверяем ответ 
    assert status == expected_answer['status']
    assert array_length == expected_answer['length'] 
    assert redis_cache == body