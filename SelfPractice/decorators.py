# https://www.youtube.com/watch?v=QH5fw9kxDQA&list=PLC0nd42SBTaNuP4iB4L6SJlMaHE71FG6N&index=2

# https://github.com/ArjanCodes/2023-decorator
"""
1. decorator patter classic using just class
2.
"""

# component
# decorator object


import functools
import logging
from time import perf_counter
from typing import Any, Callable

logger = logging.getLogger("my_app")


# def with_logging(logger: logging.Logger):
#     def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
#         @functools.wraps(func)
#         def wrapper(*args: Any, **kwargs: Any) -> Any:
#             logger.info(f"Calling {func.__name__}")
#             value = func(*args, **kwargs)
#             logger.info(f"Finished {func.__name__}")
#             return value

#         return wrapper
# return decorator


def with_logging(
    func: Callable[..., Any], logger: logging.Logger
) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.info(f"Calling {func.__name__}")
        value = func(*args, **kwargs)
        logger.info(f"Finished {func.__name__}")
        return value

    return wrapper


with_default_logging = functools.partial(with_logging, logger=logger)


def benchmark(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter()
        value = func(*args, **kwargs)
        end_time = perf_counter()
        run_time = end_time - start_time
        logging.info(
            f"Execution of {func.__name__} took {run_time:.2f} seconds.")
        return value

    return wrapper


@with_default_logging
@benchmark
def count_prime_numbers(upper_bound: int) -> int:
    count = 0
    for number in range(upper_bound):
        count += number
    return count


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    count_prime_numbers(50000)


if __name__ == "__main__":
    main()
