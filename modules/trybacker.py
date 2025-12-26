import os
import json
import time
import functools
from datetime import datetime

QUEUE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "pending_ops.json"
)


def retry_with_backoff(max_retries=3, base_delay=1.0, max_delay=60.0):
    # max_retries: Upper bound for retry attempts
    # base_delay:  Initial delay in seconds
    # max_delay:   Maximum delay cap in seconds

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        delay = min(base_delay * (2**attempt), max_delay)
                        print(
                            f"[Retry] {func.__name__} failed (attempt {attempt + 1}/{max_retries + 1}), retrying in {delay:.1f}s..."
                        )
                        time.sleep(delay)
                    else:
                        print(
                            f"[Retry] {func.__name__} failed after {max_retries + 1} attempts"
                        )
            raise last_exception

        return wrapper

    return decorator


class OfflineQueue:
    # Simple JSON-based queue for operations that failed due to connectivity issues

    def __init__(self, queue_file=QUEUE_FILE):
        self.queue_file = queue_file
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.queue_file):
            self._save([])

    def _load(self):
        try:
            with open(self.queue_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save(self, queue):
        with open(self.queue_file, "w") as f:
            json.dump(queue, f, indent=2, default=str)

    def add(self, operation, data):
        # Add a failed operation to the queue
        queue = self._load()
        queue.append(
            {
                "operation": operation,
                "data": data,
                "timestamp": datetime.now().isoformat(),
                "attempts": 0,
            }
        )
        self._save(queue)
        print(f"[Queue] Saved '{operation}' for later retry")

    def get_pending(self):
        # Get the pending operations
        return self._load()

    def remove(self, index):
        # Remove one operation (at index) after successful execution
        queue = self._load()
        if 0 <= index < len(queue):
            queue.pop(index)
            self._save(queue)

    def clear(self):
        # Clear pending operations
        self._save([])

    def is_empty(self):
        return len(self._load()) == 0


offline_queue = OfflineQueue()
