from functools import wraps
import errno
import os
import signal

from typing import Any, Callable


class ScraperTimeoutError(Exception):
    pass


def timeout(seconds: int, error_message: Exception = os.strerror(errno.ETIME)) -> Callable:
    def decorator(func):
        def _handle_timeout(signum: Any, frame: Any) -> None:
            raise TimeoutError(error_message)

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator
