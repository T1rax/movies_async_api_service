from functools import wraps
from time import sleep
from modules.logger import get_logger


logger = get_logger(__name__)


def backoff(start_sleep_time: float = 0.1,
            factor: int = 2,
            border_sleep_time: int = 10):

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            n = 0

            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    n += 1
                    logger.info(
                        f'An error {e} occurred while executing'
                        f' the function {func.__name__}'
                    )

                    if sleep_time >= border_sleep_time:
                        sleep_time = border_sleep_time
                    else:
                        sleep_time = min(
                            sleep_time * (factor ** n),
                            border_sleep_time
                        )
                    sleep(sleep_time)

        return inner

    return func_wrapper
