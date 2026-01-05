from fastapi import FastAPI
from .database import engine
from . import models
from .seed_plans import seed_plans

from .users import router as user_router
from .protected import router as protected_router
from .apikeys import router as apikey_router
from .apikey_manage import router as apikey_manage_router
from .customer import router as customer_router
from .usage import router as usage_router
from .stripe_routes import router as stripe_router
from .upi_routes import router as upi_router

app = FastAPI(title="KeyGen SaaS")

models.Base.metadata.create_all(bind=engine)
seed_plans()

app.include_router(user_router)
app.include_router(protected_router)
app.include_router(apikey_router)
app.include_router(apikey_manage_router)
app.include_router(customer_router)
app.include_router(usage_router)
app.include_router(stripe_router)
app.include_router(upi_router)

@app.get("/")
def home():
    return {"message": "KeyGen SaaS backend with plans is running"}

@app.get("/health")
def health():
    return {"status": "ok"}
