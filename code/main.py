from fastapi import FastAPI, Request
import time
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response

app = FastAPI()

REQUEST_COUNT = Counter("request_count", "Total request count")
REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency in seconds")


# this decorator allows us to track the request cycle
# it just tell fastapi to run the function for every http request
@app.middleware("http")
async def add_metrics(request: Request, call_next):
    """
    return the response object :
    also generate our metrices

    Args:
        call_next (): method allow to call the thing in the chain of the chain.(basically next endpoint)
        request: incoming http request object
    """

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    REQUEST_COUNT.inc()
    REQUEST_LATENCY.observe(process_time)

    return response


@app.get("/")
async def greet():
    return {"welcome to vibe monitor"}


@app.get("/metrices")
async def get_metrics():
    return Response(generate_latest(), media_type="text/plain")
