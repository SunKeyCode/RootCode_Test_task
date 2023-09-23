from fastapi import APIRouter, Depends


router = APIRouter()


@router.get("/test")
def test():
    return "OK"
