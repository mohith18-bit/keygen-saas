import razorpay
import os

client = razorpay.Client(
    auth=(
        os.getenv("RAZORPAY_KEY_ID"),
        os.getenv("RAZORPAY_KEY_SECRET")
    )
)

PLAN_AMOUNT_MAP = {
    "pro": 99900,          # paise (₹999)
    "enterprise": 999900   # paise (₹9999)
}

def create_upi_order(plan: str, user_id: int):
    if plan not in PLAN_AMOUNT_MAP:
        raise ValueError("Invalid plan")

    order = client.order.create({
        "amount": PLAN_AMOUNT_MAP[plan],
        "currency": "INR",
        "receipt": f"user_{user_id}_{plan}",
        "payment_capture": 1
    })

    return order
