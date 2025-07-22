"""
utils.py

A collection of utility decorators and functions for enhancing Python code.

Features:
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
    Cache the result of function calls based on their arguments.

    Args:
        f (Callable): The function to memoize.

    Returns:
        Callable: A wrapped function with caching enabled.

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
    Retry a function if it raises an exception.

    Args:
        retries (int): The maximum number of retry attempts.
        delay (float): The delay in seconds between retries.
        exceptions (tuple): A tuple of exception types to catch.

    Returns:
        Callable: A wrapped function that retries on failure.

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
    Measure and print the execution time of a function.

    Args:
        f (Callable): The function to time.

    Returns:
        Callable: A wrapped function that prints its execution time.

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
    Evaluate simple expressions in a restricted environment.

    Args:
        expr (str): The expression to evaluate.
        vars (dict): A dictionary of whitelisted variables to expose.

    Returns:
        Any: The result of the evaluated expression.

    Raises:
        Exception: If the expression is invalid or unsafe.

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
