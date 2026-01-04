from fastapi import APIRouter, Depends
from .apikey_auth import verify_api_key
from .models import APIKey

router = APIRouter()

@router.get("/customer/data")
def get_customer_data(api_key: APIKey = Depends(verify_api_key)):
    return {
        "message": "You accessed customer data using an API key",
        "api_key_id": api_key.id,
        "user_id": api_key.user_id
    }
