from fastapi import APIRouter, Depends
from .auth import verify_token

router = APIRouter()

@router.get("/protected")
def protected_route(user_id: str = Depends(verify_token)):
    return {
        "message": "You accessed a protected route",
        "user_id": user_id
    }
