import functools
import time


def time_test(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        x = func(*args, **kwargs)
        finish = time.perf_counter()
        print(f"run time: {start - finish}")
        return x
    return wrapper
