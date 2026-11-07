import random
import time

from fastapi import FastAPI, HTTPException

app = FastAPI(title="Resiliency Patterns - Circuit Breaker & Retry")


@app.get("/healthy")
def healthy():
    return {"status": "ok"}


@app.get("/unreliable")
def unreliable():
    # Fails about 50% of the time
    if random.random() < 0.5:
        raise HTTPException(status_code=500, detail="Random failure")
    return {"status": "ok"}


@app.get("/slow")
def slow():
    # Takes 1 to 10 seconds to respond
    delay = random.randint(1, 10)
    time.sleep(delay)
    return {"status": "ok", "delay_seconds": delay}
