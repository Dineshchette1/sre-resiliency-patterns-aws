import logging
import os
import time

import pybreaker
import requests
from tenacity import (RetryError, before_sleep_log, retry,
                      retry_if_exception_type, stop_after_attempt,
                      wait_exponential_jitter)

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("client")


class BreakerLogger(pybreaker.CircuitBreakerListener):
    def state_change(self, cb, old_state, new_state):
        log.warning("Circuit breaker changed: %s -> %s", old_state.name, new_state.name)


# Opens after 3 failures in a row, tries again after 10 seconds
breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=10, listeners=[BreakerLogger()])


@breaker
def call_unreliable():
    r = requests.get(f"{BASE_URL}/unreliable", timeout=3)
    r.raise_for_status()
    return r.json()


# Up to 5 tries, wait grows 1s, 2s, 4s... plus random jitter, 5s timeout per try
@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential_jitter(initial=1, max=10),
    retry=retry_if_exception_type(requests.exceptions.RequestException),
    before_sleep=before_sleep_log(log, logging.WARNING),
)
def call_slow():
    r = requests.get(f"{BASE_URL}/slow", timeout=5)
    r.raise_for_status()
    return r.json()


def main():
    print("\n=== Retry with exponential backoff: /slow ===")
    start = time.time()
    try:
        print("Success:", call_slow(), f"(took {time.time() - start:.1f}s)")
    except RetryError:
        print("Retry failed after 5 attempts")

    print("\n=== Circuit breaker: /unreliable ===")
    stats = {"success": 0, "failed": 0, "blocked": 0}
    for i in range(1, 21):
        try:
            result = call_unreliable()
            stats["success"] += 1
            print(f"[{i}] SUCCESS {result}")
        except pybreaker.CircuitBreakerError:
            stats["blocked"] += 1
            print(f"[{i}] BLOCKED - circuit breaker is OPEN")
        except requests.exceptions.RequestException as e:
            stats["failed"] += 1
            print(f"[{i}] FAILED {e}")
        time.sleep(1)

    print("\nSummary:", stats, "| final breaker state:", breaker.current_state)


if __name__ == "__main__":
    main()
