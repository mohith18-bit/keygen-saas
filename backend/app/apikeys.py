import secrets
from fastapi import APIRouter, Depends
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

@router.post("/apikeys/create")
def create_api_key(
    user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    key_value = generate_api_key()

    api_key = APIKey(
        key=key_value,
        user_id=int(user_id)
    )

    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    return {
        "api_key": api_key.key
    }
