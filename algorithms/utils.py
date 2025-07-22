"""
utils.py

Bonus Cool Stuff:
- memoize(f): Cache results of expensive function calls.
- retry_on_failure(f, retries=3): Retry a function on failure.
- timeit(f): Benchmark how long a function takes.
- safe_eval(expr, vars): Evaluate simple expressions securely.
"""

import time
import functools
import traceback


def memoize(f):
    """
    Caches the result of function calls based on arguments.

    Example:
        @memoize
        def fib(n): ...
    """
    cache = {}

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if key not in cache:
            cache[key] = f(*args, **kwargs)
        return cache[key]

    return wrapper


def retry_on_failure(retries=3, delay=0.5, exceptions=(Exception,)):
    """
    Retries a function if it raises an exception.

    Args:
        retries (int): How many times to retry.
        delay (float): Delay in seconds between retries.
        exceptions (tuple): Exception types to catch.

    Example:
        @retry_on_failure(retries=5)
        def flaky(): ...
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts <= retries:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts > retries:
                        raise
                    print(f"[retry_on_failure] Attempt {attempts} failed: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator


def timeit(f):
    """
    Prints the execution time of a function.

    Example:
        @timeit
        def do_work(): ...
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = f(*args, **kwargs)
        end = time.perf_counter()
        print(f"[timeit] {f.__name__} took {(end - start):.4f} seconds.")
        return result

    return wrapper


def safe_eval(expr: str, vars: dict = {}) -> any:
    """
    Evaluates simple expressions in a safe environment.

    Args:
        expr (str): The expression to evaluate.
        vars (dict): Whitelisted variables to expose.

    Returns:
        The result of the evaluated expression.

    Example:
        safe_eval("a + b", {"a": 2, "b": 3}) -> 5
    """
    allowed_builtins = {"abs", "min", "max", "round", "len", "sum"}
    safe_globals = {k: __builtins__[k] for k in allowed_builtins if k in __builtins__}
    safe_globals.update(vars)
    try:
        return eval(expr, {"__builtins__": safe_globals}, {})
    except Exception as e:
        print(f"[safe_eval] Error evaluating expression: {e}")
        return None
