import random

from fastapi import FastAPI, HTTPException

app = FastAPI(title="Resiliency Patterns - Graceful Degradation")


@app.get("/")
def root():
    return {"message": "Graceful degradation API is running"}


# Tier 1 - critical, always works
@app.get("/product-info")
def product_info():
    return {"product": "iPhone 16", "price": "$650", "availability": "In stock"}


# Tier 2 - important, fails about 30% of the time
@app.get("/reviews")
def reviews():
    if random.random() < 0.3:
        raise HTTPException(status_code=503, detail="Reviews service unavailable")
    return {"reviews": ["Great phone", "Battery lasts all day"]}


# Tier 3 - nice to have, fails about 70% of the time
@app.get("/recommendations")
def recommendations():
    if random.random() < 0.7:
        raise HTTPException(status_code=503, detail="Recommendations service overloaded")
    return {"recommendations": ["AirPods", "Phone case", "Fast charger"]}


# Fake CPU load so the client can decide what to show
@app.get("/system-load")
def system_load():
    return {"cpu_percent": random.randint(10, 99)}
