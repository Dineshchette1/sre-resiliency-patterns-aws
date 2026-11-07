import os
import time

import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

CACHED_REVIEWS = {"reviews": ["Cached review 1", "Cached review 2"], "fallback": True}


def get(path):
    r = requests.get(f"{BASE_URL}{path}", timeout=3)
    r.raise_for_status()
    return r.json()


def get_load():
    try:
        return get("/system-load")["cpu_percent"]
    except requests.exceptions.RequestException:
        # If we can't read the load, play it safe and assume it's high
        return 100


def render_page():
    load = get_load()
    print(f"\n[System load: {load}%]")

    if load > 80:
        tiers = 1
        print("HIGH load - serving Tier 1 only")
    elif load >= 60:
        tiers = 2
        print("MEDIUM load - serving Tier 1 and Tier 2")
    else:
        tiers = 3
        print("LOW load - serving all tiers")

    # Tier 1 - product info
    try:
        print("Product info:", get("/product-info"))
    except requests.exceptions.RequestException:
        print("Product info: temporarily unavailable")

    # Tier 2 - reviews, fall back to cached reviews
    if tiers >= 2:
        try:
            print("Reviews:", get("/reviews"))
        except requests.exceptions.RequestException:
            print("Reviews (fallback):", CACHED_REVIEWS)

    # Tier 3 - recommendations, hide quietly if they fail
    if tiers >= 3:
        try:
            print("Recommendations:", get("/recommendations"))
        except requests.exceptions.RequestException:
            print("Recommendations: hidden (service unavailable)")


if __name__ == "__main__":
    for _ in range(6):
        render_page()
        time.sleep(1)
