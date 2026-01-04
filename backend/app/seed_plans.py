from .database import SessionLocal
from .models import Plan

def seed_plans():
    db = SessionLocal()

    if db.query(Plan).count() == 0:
        db.add_all([
            Plan(name="free", quota_limit=100),
            Plan(name="pro", quota_limit=10_000),
            Plan(name="enterprise", quota_limit=1_000_000)
        ])
        db.commit()

    db.close()
