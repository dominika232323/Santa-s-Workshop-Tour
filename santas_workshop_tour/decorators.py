import functools
import time

from loguru import logger


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        logger.info(f"Finished {func.__qualname__} in {run_time:.4f} secs")
        return value, run_time
    return wrapper_timer
