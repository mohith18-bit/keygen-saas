from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import APIKey, User, Plan
from .auth import verify_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/apikeys/usage")
def get_usage(
    user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == int(user_id)).first()
    plan = db.query(Plan).filter(Plan.id == user.plan_id).first()

    keys = db.query(APIKey).filter(APIKey.user_id == user.id).all()

    return [
        {
            "key_id": key.id,
            "usage_count": key.usage_count,
            "quota_limit": plan.quota_limit,
            "remaining": plan.quota_limit - key.usage_count,
            "is_active": key.is_active
        }
        for key in keys
    ]
