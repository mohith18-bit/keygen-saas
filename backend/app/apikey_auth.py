from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import APIKey, User, Plan

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_api_key(
    x_api_key: str = Header(..., alias="X-API-Key"),
    db: Session = Depends(get_db)
):
    api_key = db.query(APIKey).filter(
        APIKey.key == x_api_key,
        APIKey.is_active == True
    ).first()

    if not api_key:
        raise HTTPException(status_code=403, detail="Invalid or revoked API key")

    user = db.query(User).filter(User.id == api_key.user_id).first()
    plan = db.query(Plan).filter(Plan.id == user.plan_id).first()

    if api_key.usage_count >= plan.quota_limit:
        raise HTTPException(status_code=403, detail="Plan quota exceeded")

    api_key.usage_count += 1
    db.commit()

    return api_key
