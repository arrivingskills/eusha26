# Real-world decorator examples: timing, logging, access control, retry logic

import functools
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


# ============================================================
# 1. TIMING — measure how long a function takes
# ============================================================


def timer(fn):
    """Print the execution time of the decorated function."""

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{fn.__name__} took {elapsed:.4f}s")
        return result

    return wrapper


@timer
def slow_sum(n):
    return sum(range(n))


slow_sum(10_000_000)  # slow_sum took 0.xxxx s


# ============================================================
# 2. LOGGING — log calls, arguments, return values, and errors
# ============================================================


def log_call(fn):
    """Log every call with its arguments and return value."""

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        arg_repr = [repr(a) for a in args]
        kwarg_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(arg_repr + kwarg_repr)
        logger.info("Calling %s(%s)", fn.__name__, signature)
        try:
            result = fn(*args, **kwargs)
            logger.info("%s returned %r", fn.__name__, result)
            return result
        except Exception as exc:
            logger.error(
                "%s raised %s: %s", fn.__name__, type(exc).__name__, exc
            )
            raise

    return wrapper


@log_call
def divide(a, b):
    return a / b


divide(10, 2)  # INFO Calling divide(10, 2) / INFO divide returned 5.0

try:
    divide(
        1, 0
    )  # INFO Calling divide(1, 0) / ERROR divide raised ZeroDivisionError
except ZeroDivisionError:
    pass


# ============================================================
# 3. ACCESS CONTROL — role-based permission check
# ============================================================

# Simulated session: in a real app this would come from a request context.
_current_user: dict | None = None


def require_role(*roles):
    """Only allow execution if the current user has one of the given roles."""

    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            if _current_user is None:
                raise PermissionError("Not authenticated.")
            user_role = _current_user.get("role")
            if user_role not in roles:
                raise PermissionError(
                    f"{fn.__name__} requires role {roles}, "
                    f"but current user has role '{user_role}'."
                )
            return fn(*args, **kwargs)

        return wrapper

    return decorator


@require_role("admin", "superuser")
def delete_user(user_id: int):
    print(f"Deleted user {user_id}.")


@require_role("admin", "editor", "superuser")
def publish_post(post_id: int):
    print(f"Published post {post_id}.")


# Simulate an admin user
_current_user = {"name": "Eusha", "role": "admin"}
delete_user(42)  # Deleted user 42.
publish_post(7)  # Published post 7.

# Simulate an unprivileged user
_current_user = {"name": "Guest", "role": "viewer"}
try:
    delete_user(
        42
    )  # PermissionError: delete_user requires role ('admin', 'superuser')...
except PermissionError as e:
    print(e)


# ============================================================
# 4. RETRY — re-run on failure with configurable attempts and delay
# ============================================================


def retry(max_attempts=3, delay=1.0, exceptions=(Exception,)):
    """
    Retry the decorated function up to max_attempts times.
    Waits delay seconds between attempts.
    Only retries on the specified exception types.
    """

    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc: Exception | None = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    print(
                        f"[retry] {fn.__name__} attempt {attempt}/{max_attempts} "
                        f"failed: {exc}"
                    )
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise RuntimeError(
                f"{fn.__name__} failed after {max_attempts} attempts"
            ) from last_exc

        return wrapper

    return decorator


# Simulate a flaky network call
_call_count = 0


@retry(max_attempts=4, delay=0.05, exceptions=(ConnectionError,))
def fetch_data(url: str) -> str:
    global _call_count
    _call_count += 1
    if _call_count < 3:
        raise ConnectionError("timeout")
    return f"<html from {url}>"


result = fetch_data("example.com")
print(result)  # <html from example.com>  (after 2 retries)


# ============================================================
# 5. COMBINING THEM — stacking real-world decorators
# ============================================================


@timer
@log_call
@require_role("admin")
def reindex_database():
    """Expensive admin-only operation."""
    time.sleep(0.05)  # simulate work
    return "done"


_current_user = {"name": "Eusha", "role": "admin"}
reindex_database()
# INFO Calling reindex_database()
# INFO reindex_database returned 'done'
# reindex_database took 0.05xs
