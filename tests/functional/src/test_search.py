import pytest

from settings import test_settings

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
                {'query': 'Mashed potato'},
                {'status': 404, 'length': 0}
        )
    ]
)
@pytest.mark.asyncio
async def test_search(query_data, expected_answer, prepare_film_es, redis_clear_cache, aiohttp_helper):

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
    status, array_length, body, headers = await aiohttp_helper.make_get_request(test_settings.service_url, '/api/v1/films/search', query_data)

    # 4. Проверяем ответ 
    assert status == expected_answer['status']
    assert array_length == expected_answer['length'] 