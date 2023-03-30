import pytest
import json
from http import HTTPStatus

from settings import test_settings


@pytest.mark.parametrize(
    'test_config, film_id, expected_answer',
    [
        (
                test_settings,
                'qwerty123-5a1c-4b95-b32b-fdd89b40dddc',
                {'status': HTTPStatus.OK, 'id': 'qwerty123-5a1c-4b95-b32b-fdd89b40dddc'}
        ),
        (
                test_settings,
                'falseid123-5a1c-4b95-b32b-fdd89b40dddc',
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
async def test_film_id(test_config, film_id, expected_answer, prepare_film_es, cache_clear_cache, aiohttp_helper):

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
                {'status': HTTPStatus.OK, 'id': 'redisccachetest-5a1c-4b95-b32b-fdd89b40dddc'}
        ),
    ]
)
@pytest.mark.asyncio
async def test_film_cache(test_config, film_id, expected_answer, prepare_film_es, cache_clear_cache, aiohttp_helper, cache_helper):

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
    status, array_length, body, headers = await aiohttp_helper.make_get_request(test_config.service_url, '/api/v1/films/'+film_id)

    # 4. Проверяем наличие ключа в редисе
    cache_value = await cache_helper.get_value('get_by_id___'+film_id+'___None___None___None___None___None___None___None')
    cache_value = json.loads(cache_value)
    cache_value['id'] = cache_value.pop('uuid')

    # 5. Проверяем ответ 
    assert status == expected_answer['status']
    assert body.get('id') == expected_answer['id'] 
    assert cache_value == body


@pytest.mark.parametrize(
    'test_config, parameters, expected_answer',
    [
        (
                test_settings,
                {'page_number': 1, 'page_size': 50},
                {'status': HTTPStatus.OK, 'length': 50}
        ),
        (
                test_settings,
                {'page_number': 1, 'page_size': 20},
                {'status': HTTPStatus.OK, 'length': 20}
        ),
        (
                test_settings,
                {'page_number': 3, 'page_size': 20},
                {'status': HTTPStatus.OK, 'length': 15}
        ),
        (
                test_settings,
                {'genre': 'genre-id-1'},
                {'status': HTTPStatus.OK, 'length': 50}
        ),
        (
                test_settings,
                {'genre': 'genre-id-fake'},
                {'status': HTTPStatus.NOT_FOUND, 'length': 0}
        ),
    ]
)
@pytest.mark.asyncio
async def test_film_all_films(test_config, parameters, expected_answer, prepare_film_es, cache_clear_cache, aiohttp_helper):

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
async def test_film_sort(test_config, parameters, expected_answer, prepare_film_es, cache_clear_cache, aiohttp_helper):

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
                {'status': HTTPStatus.OK}
        ),
        (
                test_settings,
                {'page_number': 'test'},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),
        (
                test_settings,
                {'page_number': 0},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),
        (
                test_settings,
                {'page_number': -1},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),
        (
                test_settings,
                {'page_number': 100},
                {'status': HTTPStatus.NOT_FOUND}
        ),
        (
                test_settings,
                {'page_number': 1000},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),
        (
                test_settings,
                {'page_size': 50},
                {'status': HTTPStatus.OK}
        ),
        (
                test_settings,
                {'page_size': 'test'},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),
        (
                test_settings,
                {'page_size': 0},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),
        (
                test_settings,
                {'page_size': -1},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),
        (
                test_settings,
                {'page_size': 100},
                {'status': HTTPStatus.OK}
        ),
        (
                test_settings,
                {'page_size': 1000},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),
    ]
)
@pytest.mark.asyncio
async def test_film_data_validation(test_config, parameters, expected_answer, prepare_film_es, cache_clear_cache, aiohttp_helper):

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
    status, array_length, body, headers = await aiohttp_helper.make_get_request(test_config.service_url, '/api/v1/films/', parameters)

    # 4. Проверяем ответ  
    assert status == expected_answer['status'] 