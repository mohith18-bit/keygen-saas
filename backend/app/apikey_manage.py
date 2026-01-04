import secrets
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import APIKey
from .auth import verify_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_api_key():
    return secrets.token_urlsafe(32)

@router.post("/apikeys/revoke/{key_id}")
def revoke_api_key(
    key_id: int,
    user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    api_key = (
        db.query(APIKey)
        .filter(APIKey.id == key_id, APIKey.user_id == int(user_id))
        .first()
    )

    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")

    api_key.is_active = False
    db.commit()

    return {"message": "API key revoked"}

@router.post("/apikeys/rotate/{key_id}")
def rotate_api_key(
    key_id: int,
    user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    api_key = (
        db.query(APIKey)
        .filter(APIKey.id == key_id, APIKey.user_id == int(user_id))
        .first()
    )

    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")

    api_key.key = generate_api_key()
    api_key.is_active = True
    db.commit()
    db.refresh(api_key)

    return {
        "message": "API key rotated",
        "new_api_key": api_key.key
    }
