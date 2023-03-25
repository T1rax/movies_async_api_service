import pytest
import json

from settings import test_settings


@pytest.mark.parametrize(
    'test_config, film_id, expected_answer',
    [
        (
                test_settings,
                'qwerty123-5a1c-4b95-b32b-fdd89b40dddc',
                {'status': 200, 'id': 'qwerty123-5a1c-4b95-b32b-fdd89b40dddc'}
        ),
        (
                test_settings,
                'falseid123-5a1c-4b95-b32b-fdd89b40dddc',
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
async def test_film_id(test_config, film_id, expected_answer, prepare_film_es, redis_clear_cache, aiohttp_helper):

    # 1. Генерируем данные и загружаем данные в ES (запускается 1 раз для всех тестов)
    try:
        await prepare_film_es
    except RuntimeError:
        prepare_film_es
    
    # 2. Чистим кеш редиса (запускается 1 раз для всех тестов)
    try:
        await redis_clear_cache
    except RuntimeError:
        redis_clear_cache

    # 3. Запрашиваем данные из ES по API
    status, array_length, body, headers = await aiohttp_helper.make_get_request(test_config.service_url, '/api/v1/films/'+film_id)

    # 4. Проверяем ответ 
    assert status == expected_answer['status']
    assert body.get('id') == expected_answer['id'] 


@pytest.mark.parametrize(
    'test_config, film_id, expected_answer',
    [
        (
                test_settings,
                'redisccachetest-5a1c-4b95-b32b-fdd89b40dddc',
                {'status': 200, 'id': 'redisccachetest-5a1c-4b95-b32b-fdd89b40dddc'}
        ),
    ]
)
@pytest.mark.asyncio
async def test_film_redis_cache(test_config, film_id, expected_answer, prepare_film_es, redis_clear_cache, aiohttp_helper, redis_helper):

    # 1. Генерируем данные и загружаем данные в ES (запускается 1 раз для всех тестов)
    try:
        await prepare_film_es
    except RuntimeError:
        prepare_film_es
    
    # 2. Чистим кеш редиса (запускается 1 раз для всех тестов)
    try:
        await redis_clear_cache
    except RuntimeError:
        redis_clear_cache    

    # 3. Запрашиваем данные из ES по API
    status, array_length, body, headers = await aiohttp_helper.make_get_request(test_config.service_url, '/api/v1/films/'+film_id)

    # 4. Проверяем наличие ключа в редисе
    redis_cache = await redis_helper.get_value('film__'+film_id)
    redis_cache = json.loads(redis_cache)
    redis_cache['id'] = redis_cache.pop('uuid')

    # 4. Проверяем ответ 
    assert status == expected_answer['status']
    assert body.get('id') == expected_answer['id'] 
    assert redis_cache == body


@pytest.mark.parametrize(
    'test_config, parameters, expected_answer',
    [
        (
                test_settings,
                {'page_number': 1, 'page_size': 50},
                {'status': 200, 'length': 50}
        ),
        (
                test_settings,
                {'page_number': 1, 'page_size': 20},
                {'status': 200, 'length': 20}
        ),
        (
                test_settings,
                {'page_number': 3, 'page_size': 20},
                {'status': 200, 'length': 15}
        ),
        (
                test_settings,
                {'genre': 'genre-id-1'},
                {'status': 200, 'length': 50}
        ),
        (
                test_settings,
                {'genre': 'genre-id-fake'},
                {'status': 404, 'length': 0}
        ),
    ]
)
@pytest.mark.asyncio
async def test_film_all_films(test_config, parameters, expected_answer, prepare_film_es, redis_clear_cache, aiohttp_helper):

    # 1. Генерируем данные и загружаем данные в ES (запускается 1 раз для всех тестов)
    try:
        await prepare_film_es
    except RuntimeError:
        prepare_film_es
    
    # 2. Чистим кеш редиса (запускается 1 раз для всех тестов)
    try:
        await redis_clear_cache
    except RuntimeError:
        redis_clear_cache

    # 3. Запрашиваем данные из ES по API
    status, array_length, body, headers = await aiohttp_helper.make_get_request(test_config.service_url, '/api/v1/films/', parameters)

    # 4. Проверяем ответ 
    assert status == expected_answer['status']
    assert array_length == expected_answer['length']     


@pytest.mark.parametrize(
    'test_config, parameters, expected_answer',
    [
        (
                test_settings,
                {'sort': '-imdb_rating'},
                {'descending': True, 'field': 'imdb_rating'}
        ),
        (
                test_settings,
                {'sort': 'imdb_rating'},
                {'descending': False, 'field': 'imdb_rating'}
        ),
    ]
)
@pytest.mark.asyncio
async def test_film_sort(test_config, parameters, expected_answer, prepare_film_es, redis_clear_cache, aiohttp_helper):

    # 1. Генерируем данные и загружаем данные в ES (запускается 1 раз для всех тестов)
    try:
        await prepare_film_es
    except RuntimeError:
        prepare_film_es
    
    # 2. Чистим кеш редиса (запускается 1 раз для всех тестов)
    try:
        await redis_clear_cache
    except RuntimeError:
        redis_clear_cache

    # 3. Запрашиваем данные из ES по API
    status, array_length, body, headers = await aiohttp_helper.make_get_request(test_config.service_url, '/api/v1/films/', parameters)

    # 4. Проверяем ответ  
    if expected_answer['descending']:
        assert body[0][expected_answer['field']] > body[-1][expected_answer['field']]   
    else:
        assert body[0][expected_answer['field']] < body[-1][expected_answer['field']]  


@pytest.mark.parametrize(
    'test_config, parameters, expected_answer',
    [
        (
                test_settings,
                {'page_number': 1},
                {'status': 200}
        ),
        (
                test_settings,
                {'page_number': 'test'},
                {'status': 422}
        ),
        (
                test_settings,
                {'page_number': 0},
                {'status': 422}
        ),
        (
                test_settings,
                {'page_number': -1},
                {'status': 422}
        ),
        (
                test_settings,
                {'page_number': 100},
                {'status': 404}
        ),
        (
                test_settings,
                {'page_number': 1000},
                {'status': 422}
        ),
        (
                test_settings,
                {'page_size': 50},
                {'status': 200}
        ),
        (
                test_settings,
                {'page_size': 'test'},
                {'status': 422}
        ),
        (
                test_settings,
                {'page_size': 0},
                {'status': 422}
        ),
        (
                test_settings,
                {'page_size': -1},
                {'status': 422}
        ),
        (
                test_settings,
                {'page_size': 100},
                {'status': 200}
        ),
        (
                test_settings,
                {'page_size': 1000},
                {'status': 422}
        ),
    ]
)
@pytest.mark.asyncio
async def test_film_data_validation(test_config, parameters, expected_answer, prepare_film_es, redis_clear_cache, aiohttp_helper):

    # 1. Генерируем данные и загружаем данные в ES (запускается 1 раз для всех тестов)
    try:
        await prepare_film_es
    except RuntimeError:
        prepare_film_es
    
    # 2. Чистим кеш редиса (запускается 1 раз для всех тестов)
    try:
        await redis_clear_cache
    except RuntimeError:
        redis_clear_cache

    # 3. Запрашиваем данные из ES по API
    status, array_length, body, headers = await aiohttp_helper.make_get_request(test_config.service_url, '/api/v1/films/', parameters)

    # 4. Проверяем ответ  
    assert status == expected_answer['status'] 