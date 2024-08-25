from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter('request_count', 'Total number of requests')
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Latency of requests in seconds')

async def prometheus_middleware(request, call_next):
    REQUEST_COUNT.inc()  # Increment the request count
    with REQUEST_LATENCY.time():
        response = await call_next(request)
    return response
