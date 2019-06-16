import time
from functools import wraps

__all__ = ('timer', 'timelog')

class _timer:

    def __init__(self):
        self._time = None

    def start(self):
        self._start_time = time.time()

    def stop(self):
        self._time = self._get_time()
        return self._time

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        
    def _get_time(self):
        return time.time() - self._start_time

    @property
    def time(self):
        if self._time is not None:
            return self._time
        return self._get_time()


def timer():
    return _timer()


def timelog(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            with timer() as t:
                return function(*args, **kwargs)
        finally:
            print("{}: {} sec".format(function.__name__, t.time))
    return wrapper
