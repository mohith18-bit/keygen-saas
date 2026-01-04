import stripe
import os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

PRICE_MAP = {
    "pro": "price_1Slt5aAjGRVjyyWNnoq81mV4",
    "enterprise": "price_1Slt6dAjGRVjyyWNrEvmCRd2"
}

def create_checkout_session(plan: str, user_id: int):
    if plan not in PRICE_MAP:
        raise ValueError("Invalid plan")

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price": PRICE_MAP[plan],
            "quantity": 1,
        }],
        mode="payment",
        success_url=f"https://keygen-saas.onrender.com/stripe/success?plan={plan}&user_id={user_id}",
        cancel_url="https://keygen-saas.onrender.com/stripe/cancel",
    )

    return session.url
