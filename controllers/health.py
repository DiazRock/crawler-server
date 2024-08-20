from fastapi import APIRouter

router = APIRouter()

@router.get("/isalive")
def is_alive():
    return {"status": "Server is alive"}
