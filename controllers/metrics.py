from prometheus_client.exposition import generate_latest
from starlette.responses import PlainTextResponse
from fastapi import APIRouter

router = APIRouter()

@router.get("/metrics")
async def metrics():
    return PlainTextResponse(generate_latest(), media_type="text/plain")
