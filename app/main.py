
import logging
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

from fastapi import FastAPI, HTTPException, Request

app = FastAPI(title="AI SRE Copilot")

http_requests_total = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"],
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai_sre_copilot")

@app.get("/metrics", include_in_schema=False)
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )



@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()
    status_code = 500

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response

    finally:
        duration_seconds = time.perf_counter() - start_time
        duration_ms = round(duration_seconds * 1000, 2)
        endpoint = request.url.path

        # Count the request
        http_requests_total.labels(
            method=request.method,
            endpoint=endpoint,
            status=str(status_code),
        ).inc()

        # Record request duration
        http_request_duration_seconds.labels(
            method=request.method,
            endpoint=endpoint,
        ).observe(duration_seconds)

        # Preserve your existing logging
        logger.info(
            "request_completed",
            extra={
                "method": request.method,
                "path": endpoint,
                "status_code": status_code,
                "duration_ms": duration_ms,
            },
        )



@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/slow")
def slow_endpoint():
    time.sleep(5)
    return {"status": "slow", "delay_seconds": 5}


@app.get("/error")
def error_endpoint():
    raise HTTPException(
        status_code=500,
        detail="Simulated internal server error",
    )
