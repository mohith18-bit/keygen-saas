from fastapi import APIRouter, Depends, Request, HTTPException
from .auth import verify_token
from .upi_service import create_upi_order
from .database import SessionLocal
from .models import User, Plan

router = APIRouter(prefix="/upi")

@router.post("/create/{plan}")
def create_upi(plan: str, user_id: str = Depends(verify_token)):
    order = create_upi_order(plan, int(user_id))
    return order

@router.post("/verify")
async def verify_upi_payment(request: Request):
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Expected JSON body with user_id and plan"
        )

    user_id = data.get("user_id")
    plan_name = data.get("plan")

    if not user_id or not plan_name:
        raise HTTPException(
            status_code=400,
            detail="Missing user_id or plan"
        )

    db = SessionLocal()
    plan = db.query(Plan).filter(Plan.name == plan_name).first()
    user = db.query(User).filter(User.id == int(user_id)).first()

    if not plan or not user:
        db.close()
        raise HTTPException(status_code=400, detail="Invalid data")

    user.plan_id = plan.id
    db.commit()
    db.close()

    return {"status": "success", "plan": plan_name}
    db.commit()
    db.close()

    return {"status": "success"}
