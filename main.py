from fastapi import FastAPI
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.api.v1 import address as address_router

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

# create tables (for demo/simple deployments)
Base.metadata.create_all(bind=engine)

app.include_router(address_router.router, prefix="/api/v1/addresses", tags=["addresses"])

@app.get("/healthz", tags=["health"])
def healthz():
    return {"status": "ok"}
