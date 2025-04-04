import functools
import inspect
import time

class AOP:
    """Aspect-Oriented Programming class to intercept method calls."""

    @staticmethod
    def log_method_call(func):
        """
        A decorator to log the method input parameters, output results, and calling file.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            frame = inspect.stack()[1]  # Get the caller's frame
            module = inspect.getmodule(frame[0])
            filename = module.__file__ if module else "Unknown"

            print(f"Calling method: {func.__name__} from file: {filename}")
            print(f"Input args: {args}, kwargs: {kwargs}")
            result = func(*args, **kwargs)
            print(f"Output result: {result}")
            return result
        return wrapper

    @staticmethod
    def log_execution_time(func):
        """
        A decorator to log the execution time of the method and calling file.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            frame = inspect.stack()[1]  # Get the caller's frame
            module = inspect.getmodule(frame[0])
            filename = module.__file__ if module else "Unknown"

            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"Execution time for {func.__name__} was: {end_time - start_time} seconds")
            return result
        return wrapper