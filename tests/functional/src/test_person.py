import pytest
import json
from http import HTTPStatus

from settings import test_settings


@pytest.mark.parametrize(
    'test_config, person_id, expected_answer',
    [
        (
                test_settings,
                'person-id-1',
                {'status': HTTPStatus.OK, 'id': 'person-id-1'}
        ),
        (
                test_settings,
                'person-id-222',
                {'status': HTTPStatus.NOT_FOUND, 'id': None}
        ),
        (
                test_settings,
                '111222333',
                {'status': HTTPStatus.NOT_FOUND, 'id': None}
        )
    ]
)
@pytest.mark.asyncio
async def test_person_id(test_config, person_id, expected_answer, prepare_person_es, cache_clear_cache, aiohttp_helper):
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
    status, array_length, body, headers = await aiohttp_helper.make_get_request(test_config.service_url,
                                                                                '/api/v1/persons/' + person_id)

    # 4. Проверяем ответ
    assert status == expected_answer['status']
    assert body.get('id') == expected_answer['id']


@pytest.mark.parametrize(
    'test_config, person_id, expected_answer',
    [
        (
                test_settings,
                'person-id-1',
                {'status': HTTPStatus.OK, 'id': 'person-id-1'}
        )
    ]
)
@pytest.mark.asyncio
async def test_person_id_cache(test_config, person_id, expected_answer, prepare_person_es, cache_clear_cache,
                                    aiohttp_helper, cache_helper):
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
    status, array_length, body, headers = await aiohttp_helper.make_get_request(test_config.service_url,
                                                                                '/api/v1/persons/' + person_id)

    # 4. Проверяем наличие ключа в редисе
    cache_value = await cache_helper.get_value('get_by_id___None___None___' + person_id + '___None___None___None___None___None')
    cache_value = json.loads(cache_value)
    cache_value['id'] = cache_value.pop('uuid')

    # 5. Проверяем ответ
    assert status == expected_answer['status']
    assert cache_value['id'] == expected_answer['id']


@pytest.mark.parametrize(
    'test_config, person_id, expected_answer',
    [
        (
                test_settings,
                'person-id-1',
                {'status': HTTPStatus.OK, 'length': 2}
        )
    ]
)
@pytest.mark.asyncio
async def test_person_films(test_config, person_id, expected_answer, prepare_person_es, cache_clear_cache, aiohttp_helper):
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
    status, array_length, body, headers = await aiohttp_helper.make_get_request(test_config.service_url,
                                                                                '/api/v1/persons/' + person_id + '/film')

    # 4. Проверяем ответ
    assert status == expected_answer['status']
    assert array_length == expected_answer['length']


@pytest.mark.parametrize(
    'test_config, person_id, expected_answer',
    [
        (
                test_settings,
                'person-id-1',
                {'status': HTTPStatus.OK, 'length': 2}
        )
    ]
)
@pytest.mark.asyncio
async def test_person_films_cache(test_config, person_id, expected_answer, prepare_person_es, cache_clear_cache,
                                    aiohttp_helper, cache_helper):
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
    status, array_length, body, headers = await aiohttp_helper.make_get_request(test_config.service_url,
                                                                                '/api/v1/persons/' + person_id + '/film')

    # 4. Проверяем наличие в редисе
    cache_value = await cache_helper.get_value('get_persons_films___None___None___' + person_id + '___None___None___None___None___None')
    cache_value = len(json.loads(cache_value))

    # 5. Проверяем ответ
    assert status == expected_answer['status']
    assert cache_value == expected_answer['length']