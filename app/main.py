import time
from typing import Union

from prometheus_client import Histogram, make_asgi_app
from fastapi import FastAPI

app = FastAPI()

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

REQUEST_LATENCY = Histogram(
    name='request_latency_seconds',
    documentation='Time spent processing a request',
    buckets=(.1, .2, .3, .4, .5)
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
@REQUEST_LATENCY.time()
def read_item(item_id: int, q: Union[str, None] = None):
    time.sleep(item_id / 100)
    return {"item_id": item_id, "q": q}
