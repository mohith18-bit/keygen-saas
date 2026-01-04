from fastapi import APIRouter, Depends
from .auth import verify_token
from .stripe_service import create_checkout_session

router = APIRouter(prefix="/stripe")

@router.post("/checkout/{plan}")
def checkout(plan: str, user_id: str = Depends(verify_token)):
    url = create_checkout_session(plan, int(user_id))
    return {"checkout_url": url}

@router.get("/success")
def success(plan: str, user_id: int):
    return {
        "message": "Payment successful",
        "plan": plan,
        "user_id": user_id
    }

@router.get("/cancel")
def cancel():
    return {"message": "Payment cancelled"}
